# cli_wrapper.py
import os
import sys
import time
import subprocess
import speech_recognition as sr
from services.tts_engine import speak
from services.network import is_online, send_to_cloud
from routes.offline import handle
from config import CLOUD_SERVER_URL

TRIGGER = "hey nova"
SERVER_START_DELAY = 2

server_url = CLOUD_SERVER_URL
server_online = False  # Track if cloud backend is reachable


# ---------------------------
# Ask user for backend URL if needed
# ---------------------------
def get_backend_url():
    """Check default URL; if unreachable, prompt user; allow empty input for offline."""
    global server_url, server_online

    print(f"[INFO] Trying backend server from config: {server_url}")
    if is_online():
        server_online = True
        print(f"[INFO] Server reachable at {server_url}")
        return

    # Server unreachable; prompt user
    user_input = input(
        "[INPUT] Server unreachable. Enter backend URL or leave empty for offline mode: "
    ).strip()
    if not user_input:
        server_online = False
        print("[INFO] Running in offline mode only.")
        return

    if not user_input.startswith("https"):
        user_input = "https://" + user_input

    server_url = user_input
    if is_online():
        server_online = True
        print(f"[INFO] Server reachable at {server_url}")
    else:
        server_online = False
        print("[WARN] Could not reach server. Running offline.")


# ---------------------------
# Start Flask backend (optional)
# ---------------------------
def start_server():
    if os.path.exists("app.py"):
        print("[INFO] Starting local server...")
        return subprocess.Popen([sys.executable, "app.py"])
    return None


# ---------------------------
# Voice Input Utilities
# ---------------------------
def listen_from_mic(timeout=5, phrase_time_limit=10):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(
                source, timeout=timeout, phrase_time_limit=phrase_time_limit
            )
            text = r.recognize_google(audio)
            return text.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            print("[ERROR] Speech recognition failed.")
            return ""


def listen_for_trigger(timeout=5):
    print("[INFO] Listening for trigger word...")
    text = listen_from_mic(timeout)
    if TRIGGER in text:
        print("[INFO] Trigger detected!")
        return True
    return False


def listen_for_command(timeout=5):
    print("[INFO] Listening for command...")
    text = listen_from_mic(timeout)
    if text:
        print(f"[YOU] {text}")
    else:
        print("[WARN] No command detected.")
    return text


# ---------------------------
# Command Processing
# ---------------------------
def process_command(prompt: str):
    handled, reply = handle(prompt)
    if not handled and server_online:
        try:
            reply = send_to_cloud(prompt)
        except Exception as e:
            reply = f"[Offline fallback] {reply} — cloud error: {e}"
    print(f"[ASSISTANT] {reply}")
    try:
        speak(reply)
    except Exception as e:
        print(f"[WARN] TTS failed: {e}")


# ---------------------------
# Main Loop
# ---------------------------
def main_loop():
    while True:
        if listen_for_trigger():
            cmd = listen_for_command()
            if cmd:
                process_command(cmd)


# ---------------------------
# Entry Point
# ---------------------------
def main():
    get_backend_url()

    server = start_server()
    if server:
        time.sleep(SERVER_START_DELAY)

    print(f"[INFO] Assistant is ready. Say the trigger word '{TRIGGER}' to start.")
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down...")
    finally:
        if server:
            server.terminate()


if __name__ == "__main__":
    main()
