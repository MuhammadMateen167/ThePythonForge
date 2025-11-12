import speech_recognition as sr


def listen_once(timeout=5, phrase_time_limit=10):
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(
                source, timeout=timeout, phrase_time_limit=phrase_time_limit
            )
        text = r.recognize_google(audio)
        return text
    except Exception as e:
        return f"[transcription error: {e}]"
    pass
