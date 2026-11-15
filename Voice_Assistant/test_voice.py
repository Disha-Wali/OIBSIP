
import pyttsx3

engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 180)
engine.setProperty('volume', 1.0)

engine.say("Hello! I can speak properly.")
engine.runAndWait()

print("Voice test completed!")
