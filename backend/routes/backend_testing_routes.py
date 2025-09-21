from flask import Blueprint, jsonify
from sqlalchemy import text
from models import db

# Create blueprint
testing_bp = Blueprint('testing', __name__, url_prefix='/api/test')

@testing_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Backend is running!"})

@testing_bp.route('/data', methods=['GET'])
def get_data():
    return jsonify({"data": "Hello from Flask backend!"})

@testing_bp.route('/db', methods=['GET'])
def test_database():
    try:
        result = db.session.execute(text("SELECT 1"))
        return jsonify({"status": "success", "message": "Database connected!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500