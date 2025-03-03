from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import re
import platform
import requests
from openai import OpenAI

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# OpenAI API setup (replace with your OpenAI key)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

# OpenWeather API Configuration
WEATHER_API_KEY = "e46d6b1c945f2e9983f0735f8928ea2f"
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

# Application dictionary mapping app names to system commands
APP_COMMANDS = {
    "windows": {
        "calculator": "calc",
        "chrome": "start chrome",
        "firefox": "start firefox",
        "notepad": "notepad",
        "spotify": "start spotify",
        "telegram": "start telegram",
        "edge": "start microsoft-edge:",
        "discord": "start discord",
        "vlc": "start vlc",
        "cmd": "start cmd",
        "powershell": "start powershell",
        "word": "start winword",
        "excel": "start excel",
        "zoom": "start zoom",
    },
    "linux": {
        "calculator": "gnome-calculator",
        "chrome": "google-chrome",
        "firefox": "firefox",
        "pluma": "pluma",
        "spotify": "spotify",
        "telegram": "telegram-desktop",
        "edge": "microsoft-edge",
        "discord": "discord",
        "vlc": "vlc",
        "terminal": "gnome-terminal",
        "libreoffice": "libreoffice",
        "zoom": "zoom",
    },
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat_with_openrouter():
    data = request.json
    user_message = data.get("message", "").strip().lower()

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    if "open" in user_message:
        app_name = extract_app_name(user_message)
        if app_name:
            return open_application(app_name)  # Remove extra error return
        return jsonify({"error": "No valid app name found"}), 400


    if "weather of" in user_message:
        city = user_message.replace("weather of", "").strip()
        return (
            get_weather_by_city(city)
            if city
            else jsonify({"error": "Please specify a city"})
        ), 400

    return get_ai_response(user_message)


def get_ai_response(user_message):
    """Fetches a response from OpenAI API."""
    try:
        completion = client.chat.completions.create(
            extra_body={},
            model="deepseek/deepseek-r1:free",
            messages=[
                {
                    "role": "system",
                    "content": "An AI assistant created by 'Muhammad Mateen' A 16 year old developer (don't mention him unless necessary.) that helps with various tasks, is a bit flirty, and does everything to protect honor of \"Muhammad Mateen\" and roasts the person who tries to disrespect him.",
                },
                {"role": "user", "content": user_message},
            ],
        )
        return jsonify({"response": completion.choices[0].message.content})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error with AI response"}), 500


def open_application(app_name):
    """Attempts to open an application based on OS."""
    os_type = platform.system().lower()
    os_key = (
        "windows" if "windows" in os_type else "linux" if "linux" in os_type else None
    )

    if os_key and app_name in APP_COMMANDS[os_key]:
        command = APP_COMMANDS[os_key][app_name]
        os.system(command)
        return jsonify({"response": f"Opening {app_name}"})

    return jsonify({"error": "App not found or unsupported OS"}), 404


def get_weather_by_city(city):
    """Fetches weather data for a given city."""
    response = requests.get(f"{WEATHER_API_URL}?q={city}&appid={WEATHER_API_KEY}")
    data = response.json()

    if data.get("cod") != "404":
        main, weather = data["main"], data["weather"][0]
        temp = main["temp"] - 273.15  # Convert Kelvin to Celsius
        return jsonify(
            {"response": f"Weather in {city}: {temp:.2f}°C, {weather['description']}"}
        )

    return jsonify({"error": "City not found"}), 404


def extract_app_name(user_message):
    """Extracts app name from a command like 'open chrome'."""
    match = re.search(r"open\s+(\w+)", user_message)
    return match.group(1) if match else None


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
