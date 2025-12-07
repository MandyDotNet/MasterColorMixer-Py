
import threading # to manage concurrent operations
import pyttsx3 # https://pyttsx3.readthedocs.io/en/latest/engine.html

# create a single instance of the TTS engine
_engine = pyttsx3.init()
_lock = threading.Lock() # prevent multi-thread execution of code

def speak(text: str) -> None:
    with _lock:
        _engine.say(text)
        _engine.runAndWait()

def speak_color_name(name: str) -> None:
    speak(name)