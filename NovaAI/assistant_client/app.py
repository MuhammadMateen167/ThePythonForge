import os
import sys
import json
import requests
from flask import Flask
from routes.chat import chat_bp
from routes.voice import voice_bp
from routes.download import dl_bp as download_bp
from routes.commands import commands_bp
from routes.ui import ui_bp
from services.network import set_backend_url  # <-- ensure dynamic update

# ---------------------------
# Config file paths
# ---------------------------
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"CLOUD_SERVER_URL": "http://127.0.0.1:8000"}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)


config = load_config()
server_url = config.get("CLOUD_SERVER_URL", "http://127.0.0.1:8000")
server_online = False


# ---------------------------
# Backend server validation
# ---------------------------
def get_backend_url():
    """Check default URL; if unreachable, prompt user; allow empty input for offline."""
    global server_url, server_online

    print(f"[INFO] Trying backend server from config: {server_url}")
    try:
        r = requests.get(server_url, timeout=2)
        if r.status_code in (200, 404):
            server_online = True
            print(f"[INFO] Server reachable at {server_url}")
            set_backend_url(server_url)
            return server_url
    except:
        pass

    print(f"[WARN] Default backend '{server_url}' is offline.")
    user_input = input(
        "[INPUT] Enter backend server URL (or press Enter to skip for offline mode): "
    ).strip()

    if not user_input:
        server_online = False
        print("[INFO] Running in offline mode only.")
        set_backend_url(None)
        return None

    if not user_input.startswith("http"):
        user_input = "http://" + user_input

    try:
        r = requests.get(user_input, timeout=2)
        if r.status_code in (200, 404):
            server_online = True
            print(f"[INFO] Server reachable at {user_input}")
            server_url = user_input
            save_config({"CLOUD_SERVER_URL": user_input})  # 💾 Save persistently
            set_backend_url(user_input)
            return user_input
        else:
            print("[WARN] Could not reach server. Running offline.")
            server_online = False
            set_backend_url(None)
            return None
    except Exception as e:
        print(f"[WARN] Connection failed ({e}). Running offline.")
        server_online = False
        set_backend_url(None)
        return None

app = Flask(__name__, template_folder='templates', static_folder='static')
app.register_blueprint(ui_bp)
app.register_blueprint(chat_bp, url_prefix='/api')
app.register_blueprint(voice_bp, url_prefix='/api')
app.register_blueprint(download_bp, url_prefix='/api')
app.register_blueprint(commands_bp, url_prefix='/api')

if __name__ == "__main__":
    get_backend_url()  # <-- Check backend before starting
    print(f"[INFO] Flask web app starting. Backend online: {server_online}")
    # Run Flask even if backend offline
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

