import pyttsx3

from config import VOICE_RATE


_engine = None


def _get_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        _engine.setProperty("rate", VOICE_RATE)
    return _engine


def speak(text):
    engine = _get_engine()
    engine.say(text)
    engine.runAndWait()
