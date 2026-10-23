# voice.py
import re
import threading

import numpy as np
import sounddevice as sd
from TTS.api import TTS

# Load model once
tts = TTS(model_name="tts_models/en/vctk/vits")

# Multi-speaker model: choose a voice (try p225, p226, p227, p228, p230)
SPEAKER = "p230"

SAMPLE_RATE = tts.synthesizer.output_sample_rate

_lock = threading.Lock()   # only one sentence plays at a time
is_speaking = False


def clean_text(text):
    text = re.sub(r"[^\x00-\x7F]+", "", text)   # remove emojis
    text = re.sub(r"[*_`#]", "", text)           # remove markdown
    return text.strip()


def speak(text):
    """Speak text and WAIT until it has finished playing."""
    global is_speaking
    text = clean_text(text)
    if not text:
        return

    with _lock:
        try:
            is_speaking = True
            wav = tts.tts(text=text, speaker=SPEAKER)   # no temp file needed
            data = np.asarray(wav, dtype=np.float32)
            sd.play(data, SAMPLE_RATE)
            sd.wait()
        except Exception as e:
            print("TTS Error:", e)
        finally:
            is_speaking = False


def stop_speaking():
    global is_speaking
    if is_speaking:
        sd.stop()
        is_speaking = False