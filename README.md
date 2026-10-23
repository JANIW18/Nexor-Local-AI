# Nexor-Local-AI
Nexor is a cross-platform, offline AI voice assistant powered by Ollama and Gemma 2 (2B). Talk to your PC naturally and control your system with voice commands. open browsers, Google, YouTube, and terminals, check the weather and time, and shut down your computer. Built with a Linux-first approach, with support for Linux, Windows, and macOS.


## Requirements

Before installing Nexor, make sure you have the following:

- **Python 3.11** - Required for the current setup.
- **Git** - To clone the repository.
- **Ollama** - To run the local AI model.
- **Gemma 2 (2B)** - Nexor's local AI model.
- **Vosk speech-recognition model** - For voice input.
- **Microphone and audio output** - For voice interaction.
- **Internet connection** - Required to download dependencies and models and access online features.

> **Python compatibility:** The current setup is designed for Python 3.11. Other Python versions, including Python 3.14, have not been verified and are not supported by the current setup.

## Installation Guide

### 1. Install Python 3.11 and Git

Install Python 3.11 and Git for your operating system.

**Linux - Ubuntu, Debian, or Kali Linux**

If Python 3.11 is available in your configured repositories, run:

```bash
sudo apt update
sudo apt install git curl python3.11 python3.11-venv
```

**Windows**

- Install Python 3.11.
- Install Git for Windows.

**macOS**

- Install Python 3.11.
- Install Git using an official installer or package manager.

### 2. Install uv on Linux

Nexor's Linux setup uses `uv` to install Python dependencies.

Install `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart your terminal if necessary, then verify the installation:

```bash
uv --version
```

### 3. Clone the Repository

Clone the Nexor repository and navigate to the project directory:

```bash
git clone https://github.com/JANIW18/Nexor-Local-AI.git
cd Nexor-Local-AI
```

### 4. Create and Activate a Virtual Environment

A virtual environment keeps Nexor's Python dependencies separate from other projects.

**Linux - Ubuntu, Debian, or Kali Linux**

```bash
uv venv .venv --python 3.11
source .venv/bin/activate
```

Alternatively, use Python's built-in virtual-environment tool:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

**Windows - PowerShell**

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell activation is blocked, use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

**macOS**

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 5. Install Dependencies

Ensure the virtual environment is activated before installing the dependencies.

**Linux - Using uv**

```bash
uv pip install -r requirements.txt
```

**Windows and macOS - Using pip**

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 6. Install Ollama and Download Gemma 2 (2B)

Nexor uses Ollama to run Gemma 2 (2B) locally.

**Step 1: Install Ollama**

Download and install Ollama from the official website:

https://ollama.com/

**Step 2: Download the AI model**

```bash
ollama pull gemma2:2b
```

**Step 3: Verify the model**

```bash
ollama list
```

Confirm that `gemma2:2b` appears in the list. Ensure Ollama is running before starting Nexor.

### 7. Download and Configure the Vosk Model

Nexor uses Vosk for speech recognition. You must download the speech-recognition model separately.

**Step 1: Visit the official Vosk model page**

https://alphacephei.com/vosk/models

**Step 2: Download a compatible model**

Choose a model that matches Nexor's language and configuration.

**Step 3: Extract the archive**

Extract the downloaded model archive.

**Step 4: Place the model in the project directory**

Place the extracted model folder inside `Nexor-Local-AI`, alongside `jarvis_voice.py`.

Your project structure should look similar to this:

```text
Nexor-Local-AI/
├── jarvis_voice.py
├── voice.py
├── commands.py
├── requirements.txt
├── README.md
└── vosk-model-small-en-us-0.15/
```

**Important:**

- The Vosk folder name shown above is an example. Use the actual folder name of your downloaded model.
- The model's folder path must match the path configured in Nexor's source code.
- If the existing code already points to the correct folder, no code changes are necessary.
- Run Nexor from the project directory so relative paths resolve correctly.

### 8. Verify Python

With the virtual environment activated, run:

```bash
python --version
```

The expected output is:

```text
Python 3.11.x
```

### 9. Launch Nexor

Before starting Nexor, confirm that:

- Python 3.11 is active.
- The virtual environment is activated.
- All required Python dependencies are installed.
- Ollama is installed and running.
- The `gemma2:2b` model is available.
- The Vosk model is correctly configured.
- Your microphone and audio output are working.

Launch Nexor:

```bash
python jarvis_voice.py
```

## Troubleshooting

### Python Version Issues

Check your active Python version:

```bash
python --version
```

The current setup is designed for Python 3.11.

### Missing Dependencies

Activate the virtual environment and reinstall the dependencies.

**Linux:**

```bash
uv pip install -r requirements.txt
```

**Windows and macOS:**

```bash
python -m pip install -r requirements.txt
```

### AI Model Issues

Check whether the model is installed:

```bash
ollama list
```

If `gemma2:2b` is missing, download it again:

```bash
ollama pull gemma2:2b
```

Ensure Ollama is running before launching Nexor.

### Voice Recognition Issues

- Check your microphone permissions and audio configuration.
- Confirm that the Vosk model archive has been extracted correctly.
- Verify that the model folder is in the expected location.
- Ensure the folder name matches the path configured in the source code.

## Offline Usage

Nexor uses a locally hosted AI model for local AI processing.

After the required dependencies and models have been downloaded, local AI conversations and supported local operations may work without an internet connection, provided all required components are available locally.

An internet connection is still required for downloading dependencies and models and using online features, such as website access and weather updates.

## Compatibility

Nexor follows a Linux-first development approach.

- **Tested:** Debian running under Windows Subsystem for Linux (WSL), using Python 3.11.
- **Native Ubuntu:** Not yet fully verified.
- **Other Linux distributions:** Not yet fully verified.
- **Native Windows:** Not yet fully verified.
- **macOS:** Not yet fully verified.

Compatibility may vary depending on the operating system, audio configuration, and installed dependencies.

## Development Status

Nexor is an evolving project focused on building a smarter and more capable personal AI voice assistant.

Features, compatibility, and stability may change as development continues.

## License

Nexor is released under the **MIT License**. See the [`LICENSE`](LICENSE) file for details.
