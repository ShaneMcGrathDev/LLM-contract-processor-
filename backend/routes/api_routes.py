from flask import Blueprint, jsonify, request
import pandas as pd
from services.claude_service import ClaudeService
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Initialize Claude service
claude_service = ClaudeService()

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')




@api_bp.route('/upload-excel', methods=['POST'])
def check_excel_load():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file included in request'}), 400
            
        file = request.files['file']
        
        # Read Excel file into pandas DataFrame
        df = pd.read_excel(file)
        
        # Convert first row to JSON for Claude processing
        first_row = df.iloc[0].to_json()
        
        # Get Claude response
        response = claude_service.analyze_invoice_data(first_row)
        
        return jsonify({
            'message': 'File processed successfully',
            'filename': file.filename,
            'claude_response': response,
            'row_data': first_row
        }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500