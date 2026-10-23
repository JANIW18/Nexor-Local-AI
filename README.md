# Nexor-Local-AI
Nexor is a cross-platform, offline AI voice assistant powered by Ollama and Gemma 2 (2B). Talk to your PC naturally and control your system with voice commands. open browsers, Google, YouTube, and terminals, check the weather and time, and shut down your computer. Built with a Linux-first approach, with support for Linux, Windows, and macOS.

Requirements

Before installing Nexor, make sure you have:

Python 3.11

Git

Ollama

Gemma 2 (2B) AI model

Vosk speech-recognition model

A working microphone and audio output

An internet connection for downloading dependencies and models

Python requirement: Nexor's current setup supports Python 3.11 only. Other versions, including Python 3.14, are not supported by the current setup.

Installation Guide

1. Install Python 3.11 and Git

Install Python 3.11 and Git for your operating system.

Linux — Ubuntu, Debian, or Kali Linux

On distributions where Python 3.11 is available in the configured repositories:

sudo apt update
sudo apt install git curl python3.11 python3.11-venv

Windows

Install Python 3.11 and Git for Windows.

macOS

Install Python 3.11 and Git using the appropriate official installer or package manager.

2. Install uv on Linux

Nexor's Linux installation instructions use uv to install Python dependencies.

Install uv:

curl -LsSf https://astral.sh/uv/install.sh | sh

Restart your terminal if necessary, then verify the installation:

uv --version

3. Clone the Repository

Clone Nexor from GitHub and enter the project directory:

git clone https://github.com/JANIW18/Nexor-Local-AI.git
cd Nexor-Local-AI

4. Create and Activate a Virtual Environment

A virtual environment isolates Nexor's Python dependencies from other projects.

Linux — Ubuntu, Debian, or Kali Linux

uv venv .venv --python 3.11
source .venv/bin/activate

If you prefer the standard Python virtual-environment tool:

python3.11 -m venv .venv
source .venv/bin/activate

Windows — PowerShell

py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

If PowerShell activation is blocked, use Command Prompt:

.venv\Scripts\activate.bat

macOS

python3.11 -m venv .venv
source .venv/bin/activate

5. Install Dependencies

Make sure the virtual environment is activated before installing dependencies.

Linux — using uv

uv pip install -r requirements.txt

Windows and macOS — using pip

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

6. Download the Gemma 2 (2B) AI Model

Nexor uses Ollama to run Gemma 2 (2B) locally.

Step 1: Install Ollama from the official website:

https://ollama.com/

Step 2: Download the model:

ollama pull gemma2:2b

Step 3: Verify that the model is available:

ollama list

Confirm that gemma2:2b appears in the list and ensure Ollama is running before launching Nexor.

7. Download the Vosk Speech-Recognition Model

Nexor uses Vosk for speech recognition. The Vosk model must be downloaded separately.

Step 1: Visit the official Vosk model page:

https://alphacephei.com/vosk/models

Step 2: Download a model compatible with Nexor's language and configuration.

Step 3: Extract the downloaded archive.

Step 4: Place the extracted model folder inside the Nexor-Local-AI project directory, alongside jarvis_voice.py.

Your project directory should look similar to this:

Nexor-Local-AI/
├── jarvis_voice.py
├── voice.py
├── commands.py
├── requirements.txt
├── README.md
└── vosk-model-small-en-us-0.15/

The Vosk folder name above is only an example. Use the actual folder name of the model you downloaded.

Important: The folder name must match the path configured in Nexor's source code. If the code already uses the correct relative path, no code changes are necessary. Run Nexor from the project directory.

8. Verify the Python Version

With the virtual environment activated, run:

python --version

The expected output is:

Python 3.11.x

9. Run Nexor

Before launching Nexor, ensure that:

Python 3.11 is being used.

The virtual environment is activated.

All required Python dependencies are installed.

Ollama is installed and running.

The gemma2:2b model is available.

The Vosk model is downloaded and configured correctly.

Your microphone and audio output are working.

Start Nexor:

python jarvis_voice.py

Troubleshooting

Python Version Issues

Check the active Python version:

python --version

The current setup requires Python 3.11.

Missing Dependencies

Activate the virtual environment and reinstall the dependencies.

Linux:

uv pip install -r requirements.txt

Windows and macOS:

python -m pip install -r requirements.txt

AI Model Issues

Check whether the Gemma model is installed:

ollama list

If it is missing, download it again:

ollama pull gemma2:2b

Voice Recognition Issues

Check your microphone permissions and audio configuration.

Ensure the Vosk model archive was extracted correctly.

Confirm that the model folder is in the expected location.

Check that the folder name matches the path in the source code.

Offline Usage

Nexor is designed to use a locally hosted AI model.

After the required dependencies and models have been downloaded, local AI conversations and supported local operations can work without an internet connection, provided all required components are available locally.

An internet connection is still required to download dependencies and models and to use online features such as weather updates and website access.

Compatibility

Nexor is currently developed with a Linux-first approach.

The tested environment is Debian running under Windows Subsystem for Linux (WSL), using Python 3.11. Native Ubuntu, other Linux distributions, native Windows, and macOS have not yet been fully verified.

Development Status

Nexor is an evolving project focused on building a smarter and more capable personal AI voice assistant. Features, compatibility, and stability may change as development continues.

License

This project is licensed under the MIT License. See the LICENSE file for details.
