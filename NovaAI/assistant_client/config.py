# Local client configuration - edit only when you know what you're doing.
import json
import os


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"CLOUD_SERVER_URL": None}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)


CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
CLOUD_SERVER_URL = "http://127.0.0.1:8000"
LOCAL_PORT = 5000
ENABLE_VOICE = True
VOICE_RATE = 160

config = load_config()
CLOUD_SERVER_URL = config.get("CLOUD_SERVER_URL")
