#api_routes.py

# main flask packages 
from flask import Blueprint, jsonify, request
from models import db, Invoice
from datetime import datetime


#OCR packages
from PIL import Image
import pytesseract  # For OCR


# Configure Tesseract OCR
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Configure OCR settings for better invoice recognition
custom_osd_params = '--oem 3 --psm 6'  # Use neural net LSTM engine with uniform block of text mode

# Inputs for PDF support 
import PyPDF2
from io import BytesIO

from anthropic import Anthropic

#Added for claude_test route
import pandas as pd
import json
import io
import time


#services: mainly LLM specific and database logic
from services.claude_service import ClaudeService
from services.database_service import DatabaseService
from services.field_mapping_service import FieldMappingService # NEW IMPORT

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
field_mapping_service = FieldMappingService()  # NEW SERVICE INITIALIZATION

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
    


@api_bp.route('/claude_test', methods=['POST'])
def process_invoice():
    print("=== CLAUDE_TEST ROUTE HIT ===")
    try:
        # Initialize Claude client
        from anthropic import Anthropic
        api_key = os.getenv('CLAUDE_API_KEY')
        
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'CLAUDE_API_KEY not found in environment variables'
            }), 500
        
        client = Anthropic(api_key=api_key)
        
        # Get the uploaded file
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        print(f"Processing file: {file.filename}")
        start_time = time.time()
        
        # Process based on file type
        if file.filename.endswith('.png'):
            # Process PNG file
            image = Image.open(BytesIO(file.read()))
            # Extract text using OCR
            image_text = pytesseract.image_to_string(image)
            # Use the field mapping service to optimize text
            optimized_text = field_mapping_service.optimize_excel_text_for_claude(image_text)
            data_density = 100  # Image text is considered all relevant

        elif file.filename.endswith('.pdf'):
            # Process PDF file
            pdf_text = ""
            pdf_reader = PyPDF2.PdfReader(BytesIO(file.read()))
            
            for page in pdf_reader.pages:
                pdf_text += page.extract_text() + "\n"
            
            # Use the field mapping service to optimize PDF text
            optimized_text = field_mapping_service.optimize_excel_text_for_claude(pdf_text)
            data_density = 100  # PDF text is considered all relevant
            
        else:
            # Process Excel file
            df_dict = pd.read_excel(file, sheet_name=None)
            excel_text = ""
            total_cells = 0
            non_empty_cells = 0
            
            for sheet_name, df in df_dict.items():
                print(f"Processing sheet '{sheet_name}': {len(df)} rows x {len(df.columns)} cols")
                excel_text += f"=== SHEET: {sheet_name} ===\n"
                
                for idx, row in df.iterrows():
                    row_data = []
                    has_data = False
                    
                    for col in df.columns:
                        cell_value = row[col]
                        total_cells += 1
                        
                        if pd.notna(cell_value) and str(cell_value).strip():
                            non_empty_cells += 1
                            has_data = True
                            
                            if isinstance(cell_value, (int, float)) and cell_value > 40000 and cell_value < 50000:
                                try:
                                    from datetime import datetime, timedelta
                                    excel_date = datetime(1900, 1, 1) + timedelta(days=cell_value - 2)
                                    row_data.append(f"Date:{excel_date.strftime('%Y-%m-%d')}")
                                except:
                                    row_data.append(str(cell_value))
                            else:
                                row_data.append(str(cell_value))
                        else:
                            row_data.append("")
                    
                    if has_data:
                        excel_text += f"Row {idx}: " + " | ".join(row_data) + "\n"
                
                excel_text += "\n"
            
            data_density = (non_empty_cells / total_cells * 100) if total_cells > 0 else 0
            optimized_text = field_mapping_service.optimize_excel_text_for_claude(excel_text)
        
        # Common processing for both file types
        schema_prompt = field_mapping_service.create_semantic_schema_prompt()
        detected_variations = field_mapping_service.detect_field_variations(optimized_text)
        variation_summary = field_mapping_service.get_variation_summary(detected_variations)
        
        # Limit text size
        max_chars = 3500
        if len(optimized_text) > max_chars:
            print(f"Truncating text from {len(optimized_text)} to {max_chars} chars")
            truncated_text = optimized_text[:max_chars]
            last_newline = truncated_text.rfind('\n')
            if last_newline > max_chars * 0.8:
                optimized_text = truncated_text[:last_newline]
            else:
                optimized_text = truncated_text
        
        print(f"Sending {len(optimized_text)} chars to Claude...")
        
        # Send to Claude
        claude_start = time.time()
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2500,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Extract invoice information from this {file.filename.split('.')[-1].upper()} file.
                     {f"Note: This is OCR-extracted text from an image, so there might be some recognition errors." if file.filename.endswith('.png') else ""}
                    Pay special attention to financial totals and line items. 
                    
                    {schema_prompt}
                    
                    Document Content:
                    {optimized_text}
                    """
                }
            ]
        )
        claude_time = time.time() - claude_start
        
        # Parse response
        response_text = message.content[0].text
        
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
            total_time = time.time() - start_time
            
            return jsonify({
                'success': True,
                'data': parsed_data,
                'processing_info': {
                    'detected_variations': detected_variations,
                    'variation_summary': variation_summary,
                    'file_name': file.filename,
                    'file_type': file.filename.split('.')[-1].lower(),
                    'data_density_percent': round(data_density, 1),
                    'total_processing_time': round(total_time, 2),
                    'claude_processing_time': round(claude_time, 2),
                    'text_length_sent': len(optimized_text)
                },
                'raw_response': response_text
            })
            
        except json.JSONDecodeError as json_error:
            print(f"JSON decode error: {json_error}")
            return jsonify({
                'success': False,
                'error': 'Could not parse JSON from Claude response',
                'raw_response': response_text
            }), 500
    
    except Exception as e:
        print(f"Route error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

###This is the new route to add processed invoice data to the database
@api_bp.route('/invoices', methods=['POST'])
def create_invoice():
    try:
        data = request.get_json()
        
        # Create new invoice
        invoice = Invoice(
            vendor_name=data.get('vendor_name'),
            invoice_number=data.get('invoice_number'),
            total_amount=float(data.get('total_amount', 0)),
            date=datetime.fromisoformat(data.get('date')) if data.get('date') else None,
            processed_data=data
        )
        
        # Save to database
        db.session.add(invoice)
        db.session.commit()
        
        return jsonify({
            'message': 'Invoice saved successfully',
            'invoice': invoice.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': str(e),
            'message': 'Failed to save invoice'
        }), 500
    


@api_bp.route('/review-invoice', methods=['POST'])
def review_invoice():
    """Save or update invoice data to database"""
    print("=== REVIEW INVOICE ROUTE HIT ===")
    try:
        data = request.get_json()
        
        # Validate the request data
        if not data:
            print("No data provided")
            return jsonify(format_error_response(
                'Invalid request',
                'No data provided'
            )), 400
            
        if not data.get('invoice_data'):
            print("No invoice data provided")
            return jsonify(format_error_response(
                'Invalid request',
                'No invoice data provided'
            )), 400
        
        invoice_data = data['invoice_data']
        print(f"Received invoice data: {invoice_data}")
        
        # Validate required fields
        required_fields = ['vendor_name', 'total_amount']
        missing_fields = []
        
        for field in required_fields:
            if not invoice_data.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            print(f"Missing required fields: {missing_fields}")
            return jsonify(format_error_response(
                'Validation failed',
                f'Missing required fields: {", ".join(missing_fields)}'
            )), 400
        
        # Check if this is an update (has invoice_id) or new save
        invoice_id = data.get('invoice_id')
        
        if invoice_id:
            # Update existing invoice
            print(f"Updating invoice ID: {invoice_id}")
            save_result = db_service.update_invoice(invoice_id, invoice_data)
        else:
            # Save new invoice
            print("Saving new invoice")
            save_result = db_service.save_invoice(invoice_data)
        
        if save_result['success']:
            response_data = {
                'success': True,
                'message': save_result['message'],
                'data': {
                    'invoice_id': save_result.get('invoice_id', invoice_id),
                    'saved_at': datetime.now().isoformat(),
                    'vendor_name': invoice_data.get('vendor_name'),
                    'total_amount': float(invoice_data.get('total_amount', 0))
                }
            }
            
            print(f"Invoice operation successful: {response_data}")
            return jsonify(response_data), 200
        else:
            print(f"Database operation failed: {save_result['message']}")
            return jsonify(format_error_response(
                'Database error',
                save_result['message']
            )), 500
            
    except Exception as e:
        print(f"Error in review_invoice: {str(e)}")
        return jsonify(format_error_response(
            'Server error',
            str(e)
        )), 500
