import speech_recognition as sr
import pyttsx3
import webbrowser
from urllib.parse import quote
import musiclibrary

# Initialize recognizer & speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty("rate", 150)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def processcommand(c):
    command = c.lower().strip()

    if "open google" in command or "open search" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
    elif "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        speak("Opening WhatsApp")
    elif command.startswith("play "):
        song = command[5:].strip()
        if song in musiclibrary.music:
            webbrowser.open(musiclibrary.music[song])
            speak(f"Playing {song}")
        else:
            search_query = quote(song)
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
            speak(f"Searching for {song} on YouTube")
    elif "stop" in command or "exit" in command:
        return "stop"
    else:
        speak("I did not understand that command")

    return "continue"


if __name__ == "__main__":
    speak("Activating Babygirl")

    # Adjust mic noise once at start
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                word = recognizer.recognize_google(audio).lower()
                print("Heard:", word)

            if "baby" in word or "babygirl" in word:
                speak("Yes, Babygirl. How can I help?")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = recognizer.listen(source, timeout=8, phrase_time_limit=8)
                    command = recognizer.recognize_google(audio).lower()
                    print("Command:", command)
                    status = processcommand(command)
                    if status == "stop":
                        speak("Goodbye")
                        break
            elif "stop" in word or "exit" in word:
                speak("Goodbye")
                break
        except sr.UnknownValueError:
            print("Didn't catch that, please repeat.")
        except sr.WaitTimeoutError:
            print("No speech detected, retrying...")
        except sr.RequestError as e:
            print("Could not request results; check your internet connection:", e)
        except Exception as e:
            print("Error:", e)


                    


