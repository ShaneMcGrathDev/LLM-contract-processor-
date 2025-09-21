from flask import Blueprint, jsonify, request
from models import db, NumberSubmission
from werkzeug.utils import secure_filename
import os

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/submit-number', methods=['POST'])
def submit_number():
    try:
        data = request.get_json()
        number = data.get('number')
        
        if number is None:
            return jsonify({"error": "Number is required"}), 400
        
        doubled = number * 2
        
        submission = NumberSubmission(
            number=number,
            doubled=doubled
        )
        
        db.session.add(submission)
        db.session.commit()
        
        result = {
            "id": submission.id,
            "received_number": number,
            "doubled": doubled,
            "message": f"Successfully saved number: {number}",
            "created_at": submission.created_at.isoformat()
        }
        
        return jsonify(result)
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api_bp.route('/submissions', methods=['GET'])
def get_submissions():
    try:
        submissions = NumberSubmission.query.order_by(NumberSubmission.created_at.desc()).all()
        return jsonify({
            "submissions": [submission.to_dict() for submission in submissions],
            "total": len(submissions)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/create-tables', methods=['POST'])
def create_tables():
    try:
        db.create_all()
        return jsonify({"message": "Tables created successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



@api_bp.route('/upload-png', methods=['POST'])
def upload_png():
    try:
        file = request.files['file']
        filename = secure_filename(file.filename)
        
        # Create uploads directory if it doesn't exist
        os.makedirs('uploads', exist_ok=True)
        
        file.save(f"uploads/{filename}")
        return jsonify({"message": "File uploaded!", "filename": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500