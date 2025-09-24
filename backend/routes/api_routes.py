#api_routes.py

# main flask packages 
from flask import Blueprint, jsonify, request

from anthropic import Anthropic

#Added for claude_test route
import pandas as pd
import json
import io


#services: mainly LLM specific and database logic
from services.claude_service import ClaudeService
from services.database_service import DatabaseService
from services.field_mapping_service import field_mapping_service # NEW IMPORT

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
field_mapping_service = field_mapping_service()  # NEW SERVICE INITIALIZATION

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
    




# Updated claude_test route with API key debugging
@api_bp.route('/claude_test', methods=['POST'])
def process_invoice():
    print("=== CLAUDE_TEST ROUTE HIT ===")  # Debug line
    try:
        # Check if API key is loaded
        api_key = os.getenv('CLAUDE_API_KEY')  # Changed to match your env variable
        print(f"API Key loaded: {'Yes' if api_key else 'No'}")  # Debug line
        print(f"API Key length: {len(api_key) if api_key else 0}")  # Debug line
        
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'CLAUDE_API_KEY not found in environment variables'
            }), 500
        
        # Initialize Claude client
        client = Anthropic(api_key=api_key)
        print("Claude client initialized")  # Debug line
        
        # Get the uploaded file
        if 'file' not in request.files:
            print("No file in request.files")  # Debug line
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        print(f"File received: {file.filename}")  # Debug line
        
        if file.filename == '':
            print("Empty filename")  # Debug line
            return jsonify({'error': 'No file selected'}), 400
        
        # Read Excel file
        print("Reading Excel file...")  # Debug line
        df = pd.read_excel(file, sheet_name=None)
        print(f"Excel sheets: {list(df.keys())}")  # Debug line
        
        # Convert to text format for Claude
        excel_text = ""
        for sheet_name, sheet_df in df.items():
            excel_text += f"=== SHEET: {sheet_name} ===\n"
            excel_text += sheet_df.to_string(index=False, na_rep='')
            excel_text += "\n\n"
        
        print(f"Excel text length: {len(excel_text)}")  # Debug line
        
        # Define desired output schema
        schema_prompt = """
        Extract invoice data and return as JSON with this structure:
        {
            "vendor_name": "",
            "invoice_number": "",
            "invoice_date": "",
            "due_date": "",
            "subtotal": 0,
            "freight": 0,
            "tax_amount": 0,
            "total_amount": 0,
            "line_items": [
                {
                    "description": "",
                    "quantity": 0,
                    "unit_price": 0,
                    "total": 0
                }
            ],
            "confidence": "high/medium/low"
        }
        """
        
        print("Sending request to Claude...")  # Debug line
        # Send to Claude
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Please extract invoice information from this Excel data and return it as JSON.
                    
                    {schema_prompt}
                    
                    Excel Data:
                    {excel_text[:4000]}
                    """
                }
            ]
        )
        
        print("Received response from Claude")  # Debug line
        # Parse Claude's response
        response_text = message.content[0].text
        print(f"Claude response length: {len(response_text)}")  # Debug line
        
        # Try to extract JSON from response
        try:
            if '```json' in response_text:
                json_start = response_text.find('```json') + 7
                json_end = response_text.find('```', json_start)
                json_str = response_text[json_start:json_end].strip()
            else:
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                json_str = response_text[json_start:json_end]
            
            parsed_data = json.loads(json_str)
            print("Successfully parsed JSON from Claude")  # Debug line
            
            return jsonify({
                'success': True,
                'data': parsed_data,
                'raw_response': response_text
            })
            
        except json.JSONDecodeError as json_error:
            print(f"JSON decode error: {json_error}")  # Debug line
            return jsonify({
                'success': False,
                'error': 'Could not parse JSON from Claude response',
                'raw_response': response_text
            }), 500
    
    except Exception as e:
        print(f"Route error: {str(e)}")  # Debug line
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500