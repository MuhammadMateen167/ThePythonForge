from flask import Blueprint, request, jsonify
from services.google_search import google_search
search_bp = Blueprint('search', __name__)

@search_bp.route('', methods=['POST'])
def do_search():
    data = request.get_json() or {}
    q = data.get('query','').strip()
    if not q:
        return jsonify({'error':'Missing query'}), 400
    try:
        results = google_search(q)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
