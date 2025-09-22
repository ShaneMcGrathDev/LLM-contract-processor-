from flask import Blueprint, jsonify, request
from models import db, NumberSubmission
from werkzeug.utils import secure_filename
import os

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/upload-excel', methods=['POST'])
def check_excel_load():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file included in request'}), 400
            
        file = request.files['file']
        
        # Access file properties
        print(f"Filename: {file.filename}")
        print(f"Content Type: {file.content_type}")
        
        # Read file content (as bytes)
        file_content = file.read()
        print(f"File size: {len(file_content)} bytes")
        
        # If you want to save the file
        # safe_filename = secure_filename(file.filename)
        # file.save(os.path.join('uploads', safe_filename))
        
        return jsonify({
            'message': 'File received successfully!!!!',
            'filename': file.filename,
            'content_type': file.content_type,
            'file_size': len(file_content)
        }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


