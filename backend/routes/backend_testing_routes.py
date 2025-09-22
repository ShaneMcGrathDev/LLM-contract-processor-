from flask import Blueprint, jsonify, request
from sqlalchemy import text
from models import db

# Create blueprint
testing_bp = Blueprint('testing', __name__, url_prefix='/api/test')

@testing_bp.route('/upload-excel-test', methods=['POST']) 
def check_excel_load():
    try:
        # Check if file was included in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file included in request'}), 400
            
        file = request.files['file']
        
        # Check if user submitted an empty form
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        # Return success response with file info
        return jsonify({
            'message': 'File received successfully',
            'filename': file.filename,
            'content_type': file.content_type,
            'file_size': len(file.read())
        }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500




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