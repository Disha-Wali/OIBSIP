
import webbrowser
import speech_recognition as sr
import pyttsx3
import datetime
from urllib.parse import quote_plus

# 1. Initialize voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('volume', 1.0)

# 2. Function to speak
def speak(message):
    print("Assistant:", message)

    try:
        engine.stop()
        engine.say(str(message))
        engine.runAndWait()

    except Exception as e:
        print("Voice Error:", e)
# 3. Create speech recognizer
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8

# 4. Initialize microphone
microphone = sr.Microphone()

print("\n========== VOICE ASSISTANT ==========")

with microphone as source:
    print("Calibrating microphone...")
    recognizer.adjust_for_ambient_noise(source, duration=0.5)

# 5. Initial greeting
speak("Hello! I am ready to help you.")

# 6. Continuous listening loop
while True:
    try:
        print("\nLISTENING... Speak now!", flush=True)

        # Capture voice
        with microphone as source:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=6
            )

        print("PROCESSING...", flush=True)

        # Convert voice into text
        command = recognizer.recognize_google(audio)
        command = command.lower().strip()

        print("\nYou:", command, flush=True)

        # 7. Exit command
        if any(word in command.split() for word in ["bye", "exit", "stop"]):
            speak("Goodbye! Have a nice day.")
            break

        # 8. Greeting
        elif "hello" in command or "hi" in command:
            speak("Hello! How can I help you?")

        # 9. Time
        elif "time" in command or "clock" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak("The current time is " + current_time)

        # 10. Date
        elif "date" in command or "today" in command:
            today = datetime.datetime.now().strftime("%d %B %Y")
            speak("Today's date is " + today)

        # 11. Day
        elif "day" in command:
            day = datetime.datetime.now().strftime("%A")
            speak("Today is " + day)

        # 12. Open Google
        elif "open google" in command:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        # 13. Open YouTube
        elif "open youtube" in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        # 14. Open Gmail
        elif "open gmail" in command:
            speak("Opening Gmail")
            webbrowser.open("https://mail.google.com")

        # 15. Google Search
        elif "search" in command:
            topic = command.replace("search", "", 1).strip()
            topic = topic.removeprefix("for").strip()

            if topic:
                speak("Searching Google for " + topic)
                search_url = "https://www.google.com/search?q=" + quote_plus(topic)
                webbrowser.open(search_url)
            else:
                speak("Please tell me what you want to search.")

        # 16. Assistant introduction
        elif "who are you" in command:
            speak("I am your personal voice assistant. I can tell you the time, date, search Google and open websites.")

        # 17. Capabilities
        elif "what can you do" in command:
            speak("I can answer basic questions, tell you the time and date, and open Google, YouTube and Gmail.")

        # 18. Unknown command
        else:
            speak("Sorry, I don't know how to answer that yet.")

    # 19. No speech detected
    except sr.WaitTimeoutError:
        print("UNABLE TO HEAR. Please speak again.", flush=True)

    # 20. Speech not understood
    except sr.UnknownValueError:
        print("UNABLE TO UNDERSTAND. Please repeat.", flush=True)

    # 21. Internet error
    except sr.RequestError:
        speak("Speech recognition service is unavailable. Please check your internet connection.")

    # 22. Keyboard interruption
    except KeyboardInterrupt:
        speak("Assistant stopped.")
        break

    # 23. Other errors
    except Exception as e:
        print("ERROR:", e, flush=True)
