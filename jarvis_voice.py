import os
import re
import sys
import json
import time
import queue
import random
import threading
import warnings
from datetime import datetime

import sounddevice as sd
import vosk
import ollama

import commands          # your commands.py
from voice import speak  # your Coqui TTS speak()

warnings.filterwarnings("ignore")
vosk.SetLogLevel(-1)     # hide Vosk log spam

# ------------------ Settings ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model")

LLM_MODEL = "gemma2:2b"
MAX_REPLY_TOKENS = 150      # keeps spoken answers short
MAX_HISTORY_TURNS = 6       # remembered question/answer pairs

SAMPLE_RATE = 16000
BLOCK_SIZE = 4000           # smaller block = faster reaction

# Wake word: set REQUIRE_WAKE_WORD = True to ignore TV / background talk.
REQUIRE_WAKE_WORD = False
WAKE_WORDS = ("jarvis",)
FOLLOW_UP_SECONDS = 10      # after a reply, no wake word needed for this long

MIN_WORDS_FOR_AI = 2     # ignore 1-word noise like "no" or "the" (commands still work)
ALLOWED_SHORT = {"hello", "hi", "hey", "thanks", "thank you", "good morning", "good night"}
EXIT_WORDS = ("goodbye", "exit", "quit", "stop listening")   # closes Jarvis only
CONFIRMATIONS = ["Yes Sir", "Right away, Sir", "At your command, Sir"]

SYSTEM_PROMPT = (
    "You are Jarvis, a helpful voice assistant. "
    "spoken sentences. Never use markdown, lists, or emojis. "
    "Address the user as Sir. The user's words come from speech recognition "
    "and may contain mistakes. If something sounds odd, guess the most "
    "likely meaning, or briefly ask Sir to repeat it."
)

# ------------------ Shared state ------------------
audio_q = queue.Queue()     # microphone audio
speech_q = queue.Queue()    # text waiting to be spoken
history = [{"role": "system", "content": SYSTEM_PROMPT}]


# ------------------ Audio input ------------------
def audio_callback(indata, frames, time_info, status):
    if status:
        print(status, file=sys.stderr)
    audio_q.put(bytes(indata))


def flush_audio():
    """Throw away audio captured while Jarvis was talking."""
    while True:
        try:
            audio_q.get_nowait()
        except queue.Empty:
            break


# ------------------ Speech output (background thread) ------------------
def speech_worker():
    while True:
        text = speech_q.get()
        try:
            if text is None:
                return
            speak(text)
        except Exception as e:
            print(f"TTS error: {e}")
        finally:
            speech_q.task_done()


def say(text):
    """Queue text to be spoken without blocking."""
    if text:
        speech_q.put(text)


def wait_for_speech():
    """Block until everything queued has been spoken, then clear the mic."""
    speech_q.join()
    flush_audio()


# ------------------ Text helpers ------------------
def clean_for_speech(text):
    text = re.sub(r"[^\x00-\x7F]+", "", text)      # emojis / non-ASCII
    text = re.sub(r"[*_~`#>\[\]]", "", text)        # markdown only
    text = re.sub(r"\s+", " ", text)
    return text.strip()


SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


def split_sentences(buffer, min_len=15):
    """Return (complete_sentences, leftover) from a streaming buffer."""
    parts = SENTENCE_END.split(buffer)
    complete, current = [], ""
    for part in parts[:-1]:
        current = f"{current} {part}".strip()
        if len(current) >= min_len:
            complete.append(current)
            current = ""
    leftover = f"{current} {parts[-1]}".strip()
    return complete, leftover


def trim_history():
    max_messages = 1 + MAX_HISTORY_TURNS * 2
    while len(history) > max_messages:
        del history[1:3]    # drop oldest question + answer


# ------------------ AI response (streamed, spoken sentence by sentence) ------------------
def ask_ai(user_text):
    history.append({"role": "user", "content": user_text})
    full_reply = ""
    buffer = ""

    try:
        stream = ollama.chat(
            model=LLM_MODEL,
            messages=history,
            options={"num_predict": MAX_REPLY_TOKENS},
            stream=True,
        )
        for chunk in stream:
            piece = chunk["message"]["content"]
            full_reply += piece
            buffer += piece

            sentences, buffer = split_sentences(buffer)
            for s in sentences:
                s = clean_for_speech(s)
                if s:
                    print(f"Jarvis: {s}")
                    say(s)

        tail = clean_for_speech(buffer)
        if tail:
            print(f"Jarvis: {tail}")
            say(tail)

    except Exception as e:
        history.pop()   # forget the failed question
        print(f"LLM error: {e}")
        say("Sorry Sir, I could not reach the language model. Is Ollama running?")
        return

    history.append({"role": "assistant", "content": clean_for_speech(full_reply)})
    trim_history()


# ------------------ Speech recognition ------------------
def listen(rec):
    """Wait until a full sentence is recognised and return it in lowercase."""
    flush_audio()
    rec.Reset()
    print("\nListening... (Ctrl+C to quit)")
    while True:
        data = audio_q.get()
        if rec.AcceptWaveform(data):
            text = json.loads(rec.Result()).get("text", "").strip()
            if text:
                return text.lower()


def strip_wake_word(text):
    """Return (heard_wake_word, text_without_wake_word)."""
    for w in WAKE_WORDS:
        if re.search(rf"\b{re.escape(w)}\b", text):
            cleaned = re.sub(rf"\b{re.escape(w)}\b", "", text).strip(" ,")
            return True, cleaned
    return False, text


# ------------------ Main ------------------
def main():
    try:
        model = vosk.Model(MODEL_PATH)
    except Exception as e:
        print(f"Failed to load Vosk model from {MODEL_PATH}: {e}")
        sys.exit(1)

    rec = vosk.KaldiRecognizer(model, SAMPLE_RATE)

    threading.Thread(target=speech_worker, daemon=True).start()

    hour = datetime.now().hour
    greet = ("Good morning" if hour < 12 else
             "Good afternoon" if hour < 18 else "Good evening")
    say(f"{greet}, boss. System is online.")
    wait_for_speech()

    awake_until = 0.0   # follow-up window end time

    try:
        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=BLOCK_SIZE,
            dtype="int16",
            channels=1,
            callback=audio_callback,
        ):
            while True:
                try:
                    heard = listen(rec)
                    print(f"Heard: {heard}")

                    if REQUIRE_WAKE_WORD:
                        woke, heard = strip_wake_word(heard)
                        if not woke and time.time() > awake_until:
                            continue            # ignore background talk
                        if not heard:
                            say("Yes Sir?")
                            wait_for_speech()
                            awake_until = time.time() + FOLLOW_UP_SECONDS
                            continue

                    # 1) System commands first
                    # Exit Jarvis (does NOT shut down the computer)
                    if any(re.search(rf"\b{re.escape(w)}\b", heard) for w in EXIT_WORDS):
                        say("Goodbye, Sir.")
                        wait_for_speech()
                        break

                    system_response = commands.run_command(heard)
                    if system_response:
                        print(f"System: {system_response}")
                        say(system_response)
                        wait_for_speech()
                    else:
                        # 2) Otherwise ask the AI (skip 1-word noise)
                        if len(heard.split()) < MIN_WORDS_FOR_AI and heard not in ALLOWED_SHORT:
                            print("(ignored: too short, probably noise)")
                            continue
                        ask_ai(heard)
                        wait_for_speech()

                    awake_until = time.time() + FOLLOW_UP_SECONDS

                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"Error: {e}")
                    say("Sorry, I encountered an error, Sir.")
                    wait_for_speech()

    except KeyboardInterrupt:
        print("\nShutting down...")
        say("Shutting down, Sir.")
        wait_for_speech()
    except sd.PortAudioError as e:
        print(f"Microphone error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()