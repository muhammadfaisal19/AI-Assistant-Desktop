import speech_recognition as sr
import pyttsx3
import os
import datetime
import webbrowser
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables and initialize clients
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Setup text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speak(text):
    print(f"🤖 Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
        try:
            text = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("⚠️ Didn't catch that.")
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
    return None

def openai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error contacting OpenAI: {e}"

def handle_command(command):
    now = datetime.datetime.now()
    
    if "time" in command:
        speak(f"The current time is {now.strftime('%H:%M')}")
    
    elif "date" in command:
        speak(f"Today's date is {now.strftime('%Y-%m-%d')}")

    elif "open website" in command:
        url = command.partition("open website")[-1].strip()
        if not url.startswith("http"):
            url = "https://" + url
        webbrowser.open(url)
        speak(f"Opening {url}")

    elif "search" in command:
        query = command.partition("search")[-1].strip()
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        speak(f"Searching for {query}")

    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()

    elif "tell me about" in command or "what is" in command:
        query = command.partition("tell me about")[-1].strip() or command.partition("what is")[-1].strip()
        speak(openai_response(query))

    elif "joke" in command:
        speak(openai_response("Tell me a joke"))

    elif "weather" in command:
        speak(openai_response("What's the weather like today?"))

    elif "news" in command:
        speak(openai_response("What's the latest news?"))

    elif "calculate" in command:
        expression = command.partition("calculate")[-1].strip()
        speak(openai_response(f"Calculate {expression}"))

    elif "define" in command:
        term = command.partition("define")[-1].strip()
        speak(openai_response(f"Define {term}"))

    elif "translate" in command:
        text = command.partition("translate")[-1].strip()
        speak(openai_response(f"Translate {text}"))

    elif "reminder" in command:
        task = command.partition("reminder")[-1].strip()
        speak(openai_response(f"Set a reminder for {task}"))

    elif "play music" in command:
        song = command.partition("play music")[-1].strip()
        speak(openai_response(f"Play music for {song}"))

    elif "open application" in command:
        app_name = command.partition("open application")[-1].strip()
        try:
            os.system(f"start {app_name}")
            speak(f"Opening {app_name}")
        except Exception:
            speak("Sorry, I couldn't open that application.")

    elif "what can you do" in command:
        capabilities = (
            "I can tell time, date, open websites, search the web, tell jokes, "
            "give weather and news updates, perform calculations, define words, "
            "translate languages, set reminders, play music, and open applications."
        )
        speak(capabilities)

    else:
        speak(openai_response(command))

def main():
    speak("Hello! How can I assist you today?")
    while True:
        command = listen()
        if command:
            handle_command(command)
        else:
            speak("Please say that again.")

if __name__ == "__main__":
    main()

# This code is a simple voice assistant that can respond to commands like telling the time, date,
# opening websites, searching the web, and handling general queries using OpenAI's API.
# It uses speech recognition for input and text-to-speech for output.

