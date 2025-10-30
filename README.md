# 🤖 Polo – Your Personal Voice Assistant

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Powered by Ollama](https://img.shields.io/badge/AI-Ollama-orange)](https://ollama.com)

**Polo** is an intelligent, cross-platform voice assistant built in Python.  
It listens to your voice, performs system tasks, answers questions, and chats using a local **Ollama AI model (phi3)** — all **offline**, right on your machine.

---

## ✨ Features

- 🎙️ **Speech Recognition** – Understands your voice commands  
- 💬 **AI Chat** – Responds conversationally using a local `phi3` model  
- 🔊 **Text-to-Speech (TTS)** – Speaks responses aloud  
- 🌐 **Web Shortcuts** – Quickly opens YouTube, Google, ChatGPT, and more  
- 💻 **App Launching** – Opens system apps like Calculator, Notes, Safari, etc.  
- 🕒 **Time & Date** – Tells the current time or date  
- 🎵 **YouTube Playback** – Plays any song you say  
- 🧩 **Cross-Platform** – Works on macOS, Windows, and Linux  

---

## 🧰 Requirements

### 🐍 Python Version
> Python **3.8 or higher** is recommended.

### 📦 Install Dependencies

Install all required packages:
```bash
pip install speechrecognition pyttsx3 pywhatkit pyautogui ollama
For microphone support:

bash
Copy code
pip install pyaudio
💡 macOS users: If pyaudio fails to install, run:

bash
Copy code
brew install portaudio
pip install pyaudio
🧠 Ollama Setup (for AI Chat)
Polo uses a local Ollama model for intelligent responses.

Download Ollama → https://ollama.com/download

Pull the phi3 model:

bash
Copy code
ollama pull phi3
Keep Ollama running in the background before starting Polo.

⚙️ Running Polo
Clone or download this repository, then run:

bash
Copy code
python polo.py
When Polo greets you, try speaking commands like:

🗣️ “Open YouTube”
🗣️ “What’s the time?”
🗣️ “Play Shape of You”
🗣️ “Who are you?”
🗣️ “Stop Polo”

🗣️ Supported Commands
Command Example	Action
“Open YouTube”	Opens YouTube in browser
“Play [song name]”	Plays song on YouTube
“Open calculator”	Opens Calculator
“What’s the time/date?”	Speaks current time or date
Anything else	Smart AI reply from phi3
“Stop Polo”	Gracefully exits the assistant

💻 OS Compatibility
OS	Text-to-Speech Method	App Launching
🧑‍💻 macOS	Native say command	Uses /Applications
🪟 Windows	pyttsx3 (SAPI5)	Uses system apps like calc
🐧 Linux	pyttsx3 (espeak)	Uses default desktop apps
