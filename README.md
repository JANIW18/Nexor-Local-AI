# Nexor-Local-AI
Nexor is a cross-platform, offline AI voice assistant powered by Ollama and Gemma 2 (2B). Talk to your PC naturally and control your system with voice commands. open browsers, Google, YouTube, and terminals, check the weather and time, and shut down your computer. Built with a Linux-first approach, with support for Linux, Windows, and macOS.



## Python Version Requirement

**Nexor currently supports Python 3.11.17 only.** Other Python versions, including Python 3.14, are not supported by the current setup.

## 1. Create a Virtual Environment

Make sure Python 3.11 is installed before continuing.

### Linux (Ubuntu, Debian, Kali Linux)

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### Windows (PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell activation is blocked, use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### macOS

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

## 2. Install Dependencies

With the virtual environment activated, install Nexor's dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Verify Python Version

```bash
python --version
```

The output should be:

```text
Python 3.11.x
```

**Important:** Nexor's current setup requires Python 3.11. Compatibility with other Python versions and operating systems has not been verified.
