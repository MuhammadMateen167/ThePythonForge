from flask import Blueprint, request, jsonify
from services.speech_recognition import listen_once
from services.tts_engine import speak
voice_bp = Blueprint('voice', __name__)

@voice_bp.route('/listen', methods=['POST'])
def listen_route():
    # records from default mic and returns transcribed text
    text = listen_once()
    return jsonify({'transcript': text})

@voice_bp.route('/speak', methods=['POST'])
def speak_route():
    data = request.get_json() or {}
    text = data.get('text', '')
    speak(text)
    return jsonify({'status': 'ok'})
