import speech_recognition as sr
import os
import webbrowser
import datetime
import pywhatkit
import pyttsx3
import sys
import pyautogui
import ollama
import time
import subprocess
import platform


#_______________________________________________________________________________________________________
# AI Response Function (Ollama)
def ai_response(prompt: str) -> str:
    try:
        response = ollama.chat(
            model="phi3",
            messages=[{"role": "user", "content": prompt}]
        )

        print("Raw Ollama Response:", response)

        # Case 1: Object-style response
        if hasattr(response, "message"):
            msg = response.message
            if hasattr(msg, "content"):
                return msg.content

        # Case 2: Dict-style response
        if isinstance(response, dict):
            if "message" in response:
                msg = response["message"]
                if isinstance(msg, dict) and "content" in msg:
                    return msg["content"]
                if hasattr(msg, "content"):
                    return msg.content
            elif "messages" in response:
                messages = response["messages"]
                if isinstance(messages, list) and messages:
                    last = messages[-1]
                    if isinstance(last, dict) and "content" in last:
                        return last["content"]
                    if hasattr(last, "content"):
                        return last.content

        # Fallback
        return "I understood your question, but couldn’t extract a proper answer."

    except Exception as e:
        return f"Error talking to Ollama: {e}"


#_______________________________________________________________________________________________________
# Text-to-Speech setup
system_os = platform.system().lower()
engine = None

if system_os != "darwin":  # Not macOS
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    if voices:
        print("Available voices:")
        for i, voice in enumerate(voices):
            print(f"{i}: {voice.name} ({voice.id})")
        engine.setProperty('voice', voices[0].id)
    else:
        print("No voices found for pyttsx3.")

#_______________________________________________________________________________________________________
def say(text, max_sentences=None):
    """Speaks text using macOS TTS or pyttsx3 depending on OS."""
    if not text:
        return

    # Optional trimming for long replies
    if max_sentences:
        sentences = text.replace("\n", " ").split(". ")
        text = ". ".join(sentences[:max_sentences]).strip()

    print("Speaking (truncated):", text[:120], "..." if len(text) > 120 else "")

    try:
        if system_os == "darwin":
            # macOS native TTS
            subprocess.run(['say', text])
        else:
            # Fallback to pyttsx3
            if engine:
                engine.say(text)
                engine.runAndWait()
    except Exception as e:
        print("Error speaking:", e)

    time.sleep(0.15)  # short pause to avoid overlap with mic

#_______________________________________________________________________________________________________
def take_command():
    """Listens for voice input and returns recognized text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        print("Listening...")

        try:
            audio = r.listen(source, timeout=3, phrase_time_limit=5)
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query

        except sr.WaitTimeoutError:
            print("No audio detected.")
            return ""
        except sr.UnknownValueError:
            print("Could not understand speech.")
            return ""
        except sr.RequestError:
            print("Speech recognition service unavailable.")
            return ""

#_______________________________________________________________________________________________________
def processCommand(text):
    """Handles built-in commands like date, time, open calculator, play song."""
    if "date" in text.lower():
        date = datetime.date.today()
        say(f"The date today is {date}")

    elif "time" in text.lower():
        now = datetime.datetime.now()
        hour = now.strftime("%I").lstrip("0")
        minute = now.strftime("%M")
        ampm = now.strftime("%p")

        if minute == "00":
            say(f"The time right now is {hour} o'clock {ampm}")
        else:
            say(f"The time right now is {hour}:{minute} {ampm}")

    elif "open calculator" in text.lower():
        if system_os == "darwin":
            os.system("open /System/Applications/Calculator.app")
        elif system_os == "windows":
            os.system("calc")
        else:
            os.system("gnome-calculator &")
        say("Opening calculator.")

    elif text.lower().startswith("play"):
        song = text.lower().replace("play", "").strip()
        pywhatkit.playonyt(song)
        say("Playing " + song)
    else:
        return False

    return True

#_______________________________________________________________________________________________________
def stop():
    say("Goodbye, shutting down.")
    sys.exit(0)

#_______________________________________________________________________________________________________
if __name__ == "__main__":
    say("Hello, I am Polo. How may I help you?")

    sites = [
        ["youtube", "https://www.youtube.com"],
        ["whatsapp", "https://web.whatsapp.com/"],
        ["google", "https://www.google.com"],
        ["github", "https://www.github.com"],
        ["stackoverflow", "https://stackoverflow.com"],
        ["wikipedia", "https://www.wikipedia.org"],
        ["reddit", "https://www.reddit.com"],
        ["twitter", "https://twitter.com"],
        ["linkedin", "https://www.linkedin.com"],
        ["amazon", "https://www.amazon.com"],
        ["netflix", "https://www.netflix.com"],
        ["gemini", "https://gemini.google.com"],
        ["chatgpt", "https://chat.openai.com"],
        ["instagram", "https://www.instagram.com"],
        ["facebook", "https://www.facebook.com"],
        ["spotify", "https://www.spotify.com"],
        ["news", "https://news.google.com"],
        ["gmail", "https://mail.google.com"],
        ["maps", "https://maps.google.com"]
    ]

    apps = [
        ["calculator", "open /System/Applications/Calculator.app"],
        ["safari", "open /Applications/Safari.app"],
        ["notes", "open /System/Applications/Notes.app"],
        ["calendar", "open /System/Applications/Calendar.app"],
        ["music", "open /System/Applications/Music.app"],
        ["messages", "open /System/Applications/Messages.app"],
        ["facetime", "open /System/Applications/FaceTime.app"]
    ]

    while True:
        query = take_command()
        if not query:
            continue

        if "stop" in query.lower() and "polo" in query.lower():
            stop()

        handled = False

        # Open websites
        if "open" in query.lower():
            for site in sites:
                if f"open {site[0]}" in query.lower():
                    say(f"Opening {site[0]}")
                    webbrowser.open(site[1])
                    handled = True
                    break

        # Open macOS apps
        if not handled and "open" in query.lower():
            for app in apps:
                if f"open {app[0]}" in query.lower():
                    say(f"Opening {app[0]}")
                    os.system(app[1])
                    handled = True
                    break

        # Built-in commands
        if not handled:
            handled = processCommand(query)

        # AI fallback
        if not handled:
            reply = ai_response(query)
            print("AI Response:", reply)
            speech_text = reply.replace("*", "").replace("#", "").replace("`", "")
            say(speech_text, max_sentences=2)
