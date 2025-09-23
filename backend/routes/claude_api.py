
from flask import Blueprint, jsonify

# claude_api.py
claude_api = Blueprint('claude_api', __name__, url_prefix='/api/claude')

@claude_api.route('/models', methods=['GET'])
def get_models():
    models = [
        {"id": "claude-3-5-sonnet-20241022", "name": "Claude 3.5 Sonnet"},
        {"id": "claude-3-5-haiku-20241022", "name": "Claude 3.5 Haiku"},
        {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus"}
    ]
    return jsonify({"models": models})