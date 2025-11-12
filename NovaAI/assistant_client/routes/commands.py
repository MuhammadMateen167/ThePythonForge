# routes/commands.py
from flask import Blueprint, request, jsonify
from routes.offline import handle

commands_bp = Blueprint("commands", __name__)


@commands_bp.route("/command", methods=["POST"])
def run_command_route():
    data = request.get_json()
    prompt = data.get("prompt", "")
    response = handle(prompt)  # your offline handler
    return jsonify({"response": response})  # <-- must return JSON!
