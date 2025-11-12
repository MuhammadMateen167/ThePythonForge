from flask import Blueprint, request, jsonify
from services.network import is_online, send_to_cloud
from routes.offline import handle as run_command

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/query", methods=["POST"])
def query():
    data = request.get_json() or {}
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"error": "Empty prompt"}), 400

    # 1) Try offline handler first
    handled, reply = run_command(prompt)
    if handled:
        # It was a command, return offline reply
        return jsonify({"reply": reply})

    # 2) Otherwise, try sending to cloud
    if is_online():
        try:
            reply = send_to_cloud(prompt)
            return jsonify({"reply": reply})
        except Exception as e:
            # fallback to offline if cloud fails
            return (
                jsonify({"reply": f"[Offline fallback] {reply} — cloud error: {e}"}),
                502,
            )

    # 3) Offline fallback if not online
    return jsonify({"reply": reply})
