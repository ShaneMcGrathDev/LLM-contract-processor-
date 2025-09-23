from flask import Blueprint, jsonify, request
from services.claude_service import ClaudeService
from utils.file_validator import validate_file
from utils.excel_processor import process_excel_to_string
from utils.response_formatter import format_success_response, format_error_response
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
        # Step 1: Validate file
        file = request.files.get('file')
        is_valid, error_type, error_message = validate_file(file)
        
        if not is_valid:
            return jsonify(format_error_response(error_type, error_message)), 400
        
        # Step 2: Process Excel file to string
        processing_results = process_excel_to_string(file)
        
        # Step 3: Format and return response
        response_data = format_success_response(file.filename, processing_results)
        
        # Future Claude integration point (commented out for now)
        # claude_response = claude_service.analyze_invoice_data(processing_results['claude_ready_string'])
        # response_data['claude_response'] = claude_response
        
        return jsonify(response_data), 200
            
    except Exception as e:
        error_response = format_error_response(
            'File processing failed', 
            str(e), 
            'Ensure the Excel file is valid and not corrupted'
        )
        return jsonify(error_response), 500