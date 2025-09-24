#api_routes.py

# main flask packages 
from flask import Blueprint, jsonify, request

#services: mainly LLM specific and database logic
from services.claude_service import ClaudeService
from services.database_service import DatabaseService

#utility functions 
from utils.file_validator import validate_file
from utils.excel_processor import process_excel_to_string
from utils.response_formatter import format_success_response, format_error_response
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Claude service
claude_service = ClaudeService()
db_service = DatabaseService()

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
        
        # Step 3: Get Claude's analysis
        try:
            claude_response = claude_service.analyze_invoice_data(
                processing_results['claude_ready_string']
            )
            print(f"Claude Analysis: {claude_response}")  # Debug logging
        except Exception as claude_error:
            print(f"Claude Analysis Error: {str(claude_error)}")
            claude_response = {
                "error": "Claude analysis failed",
                "details": str(claude_error)
            }
        
        # Step 4: Format complete response
        response_data = format_success_response(file.filename, processing_results)
        response_data['claude_analysis'] = claude_response
        
        return jsonify(response_data), 200
            
    except Exception as e:
        error_response = format_error_response(
            'File processing failed', 
            str(e), 
            'Ensure the Excel file is valid and not corrupted'
        )
        return jsonify(error_response), 500
    


@api_bp.route('/review-invoice', methods=['POST'])
def review_invoice():
    try:
        data = request.get_json()
        
        # Validate the edited data
        if not data.get('invoice_data'):
            return jsonify(format_error_response(
                'Invalid request',
                'No invoice data provided'
            )), 400
            
          # Save to database using service
        save_result = db_service.save_invoice(data['invoice_data'])
        
        return jsonify(save_result), 200
            
    except Exception as e:
        return jsonify(format_error_response(
            'Review failed',
            str(e)
        )), 500