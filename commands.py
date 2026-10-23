# commands.py
import re
import time
import shutil
import subprocess
import os
import webbrowser
import datetime
from urllib.parse import quote_plus

CONFIRM_TIMEOUT = 15          # seconds to answer "yes" to a dangerous command
_pending = None               # (action_name, expires_at)


def _has(command, *phrases):
    """True if any phrase appears as whole words in the command."""
    return any(re.search(rf"\b{re.escape(p)}\b", command) for p in phrases)


def _launch(args):
    """Start a program without crashing if it isn't installed."""
    try:
        subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False


def _set_pending(action):
    global _pending
    _pending = (action, time.time() + CONFIRM_TIMEOUT)


def _handle_pending(command):
    """Handle the yes/no answer to a dangerous command."""
    global _pending
    action, expires = _pending
    _pending = None

    if time.time() > expires:
        return None                       # too late, treat as a normal sentence

    if _has(command, "yes", "confirm", "do it", "proceed"):
        if action == "shutdown":
            # 6 second delay so Jarvis can finish speaking first
            subprocess.Popen(["bash", "-c", "sleep 6; systemctl poweroff"])
            return "Shutting down the computer. Goodbye, Sir."
        if action == "restart":
            subprocess.Popen(["bash", "-c", "sleep 6; systemctl reboot"])
            return "Restarting the computer, Sir."

    return "Cancelled, Sir."


def run_command(command):
    command = command.lower().strip()

    # Waiting for confirmation of shutdown / restart?
    if _pending:
        reply = _handle_pending(command)
        if reply:
            return reply

    # ---------- Dangerous: ask first ----------
    if _has(command, "shutdown", "shut down", "power off") and _has(command, "computer", "system", "pc", "laptop"):
        _set_pending("shutdown")
        return "Do you really want to shut down the computer? Say yes to confirm."

    if _has(command, "restart", "reboot") and _has(command, "computer", "system", "pc", "laptop"):
        _set_pending("restart")
        return "Do you really want to restart the computer? Say yes to confirm."

    # ---------- Apps ----------
    if _has(command, "open browser", "open chrome", "open google"):
        webbrowser.open("https://www.google.com")
        return "Opening browser."

    if _has(command, "open youtube"):
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    if _has(command, "open terminal"):
        if _launch(["gnome-terminal"]) or _launch(["x-terminal-emulator"]):
            return "Opening terminal."
        return "I could not find a terminal program."

    if _has(command, "open files", "open file manager", "open home"):
        _launch(["xdg-open", os.path.expanduser("~")])
        return "Opening your home folder."

    # ---------- Web search: "search for cats" ----------
    m = re.search(r"\bsearch (?:for )?(.+)", command)
    if m:
        query = m.group(1).strip()
        webbrowser.open(f"https://www.google.com/search?q={quote_plus(query)}")
        return f"Searching for {query}."

    # ---------- Volume ----------
    if shutil.which("pactl"):
        if _has(command, "volume up", "louder"):
            subprocess.Popen(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+10%"])
            return "Volume up."
        if _has(command, "volume down", "quieter", "lower the volume"):
            subprocess.Popen(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-10%"])
            return "Volume down."
        if _has(command, "mute"):
            subprocess.Popen(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"])
            return "Toggling mute."

    # ---------- Time and date ----------
    if _has(command, "what time", "the time", "current time", "time is it", "tell me the time"):
        now = datetime.datetime.now()
        spoken = now.strftime("%I:%M %p").lstrip("0")
        return f"The time is {spoken}."

    if _has(command, "the date", "today's date", "what day", "what date", "todays date"):
        today = datetime.date.today()
        return f"Today is {today.strftime('%A, %B %d, %Y')}."

    return None