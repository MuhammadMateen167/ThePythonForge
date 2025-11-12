from flask import Blueprint, request, jsonify
from services.openai_service import get_ai_response
ai_bp = Blueprint('ai', __name__)

@ai_bp.route('', methods=['POST'])
def chat():
    data = request.get_json() or {}
    prompt = data.get('prompt','').strip()
    if not prompt:
        return jsonify({'error':'Missing prompt'}), 400
    try:
        reply = get_ai_response(prompt)
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
