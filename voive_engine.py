import os
import pyttsx3
import speech_recognition as sr


class Voicein:
    # Voice engine
    def speak(self, text):
        try:
            print(f"Assistant: {text}")
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("speech error :", e)
            
    # Listen Function
    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.speak("I'm listening...")
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said:", text)
            return text
        except:
            self.speak("Sorry, I didn't catch that.")
            return ""
        
        
if __name__ == "__main__":
    voice_assistant = Voicein()  
    
    voice_assistant.speak("Hello there! I am your Python voice assistant.")
    user_input = voice_assistant.listen()
    voice_assistant.speak(f"You just said: {user_input}")