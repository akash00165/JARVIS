# ⚡ J.A.R.V.I.S — Desktop AI Assistant

**Just A Rather Very Intelligent System** — A full Iron Man–inspired AI desktop assistant powered by Claude.

---

## 🚀 Quick Start

### 1. Install Python
Make sure you have **Python 3.8+** installed: https://www.python.org/downloads/

### 2. Install Dependencies

```bash
pip install anthropic SpeechRecognition pyttsx3
```

For voice input (microphone), also install PyAudio:

**Windows:**
```bash
pip install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

> **Note:** Voice is optional! JARVIS works fully via text without PyAudio.

### 3. Run JARVIS

```bash
python jarvis.py
```

### 4. Configure API Key
On first launch, go to **Settings** (top right) and enter your Anthropic API key.
Get one at: https://console.anthropic.com

---

## 🎙️ Wake Word

Say **"JARVIS"** (or your custom wake word) and JARVIS will start listening for your command.

Example: *"Hey JARVIS, open my Downloads folder"*

---

## 💬 What JARVIS Can Do

### Open Files & Folders
- *"Open my resume"*
- *"Show me my Downloads folder"*
- *"Open Documents"*

### Launch Apps
- *"Open Chrome"*
- *"Launch the calculator"*
- *"Open VS Code"*
- *"Start Spotify"*

### Browse the Web
- *"Open YouTube"*
- *"Search for AI news"*
- *"Go to GitHub"*

### Answer Anything
- *"What's the weather in Mumbai?"*
- *"Explain quantum computing"*
- *"Write me a Python script to sort a list"*
- *"Help me draft an email"*

### System Tasks
- *"What files are in my Desktop?"*
- *"Run a speed test"*
- *"What's my IP address?"*

---

## 📁 Project Structure

```
jarvis/
├── jarvis.py              ← Main entry point (run this)
├── requirements.txt       ← Python dependencies
├── jarvis_config.json     ← Your settings (auto-created)
├── core/
│   ├── brain.py           ← Claude AI integration
│   ├── actions.py         ← File/app/URL opener
│   ├── voice.py           ← Speech recognition & TTS
│   └── config.py          ← Settings management
└── ui/
    └── app_window.py      ← Full GUI (tkinter)
```

---

## ⚙️ Settings

Click **SETTINGS** in the app to configure:

| Setting | Description |
|---------|-------------|
| API Key | Your Anthropic API key |
| Username | How JARVIS addresses you (e.g., "Sir", "Boss") |
| Wake Word | Word to trigger voice (default: "jarvis") |
| Voice Enabled | Toggle TTS on/off |

---

## 🛠️ Troubleshooting

**"Voice unavailable"** → Install `SpeechRecognition` and `pyaudio`

**"API authentication failed"** → Check your API key in Settings

**Can't open apps on Linux** → Make sure the app binary is in your PATH

**PyAudio install fails on macOS** → Run `brew install portaudio` first

---

## 🔐 Privacy
- Your API key is stored locally in `jarvis_config.json` only
- Conversations are not saved between sessions
- Voice processing uses Google Speech-to-Text (requires internet)

---

*Powered by Claude AI from Anthropic*
