from flask import Blueprint, jsonify, request
from models import db, NumberSubmission
from werkzeug.utils import secure_filename
import os

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/upload-excel', methods=['POST']) 
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


