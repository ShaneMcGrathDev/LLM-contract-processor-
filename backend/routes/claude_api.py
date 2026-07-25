
from flask import Blueprint, jsonify

# claude_api.py
claude_api = Blueprint('claude_api', __name__, url_prefix='/api/claude')

@claude_api.route('/models', methods=['GET'])
def get_models():
    models = [
        {"id": "claude-opus-4-8", "name": "Claude Opus 4.8"},
        {"id": "claude-sonnet-5", "name": "Claude Sonnet 5"},
        {"id": "claude-haiku-4-5", "name": "Claude Haiku 4.5"}
    ]
    return jsonify({"models": models})