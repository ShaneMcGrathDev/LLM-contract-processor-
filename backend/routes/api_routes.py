#api_routes.py

# main flask packages 
from flask import Blueprint, jsonify, request

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
        
        # OPTIMIZATION 1: More efficient Excel reading
        start_time = time.time()
        df_dict = pd.read_excel(file, sheet_name=None)
        read_time = time.time() - start_time
        print(f"Excel read time: {read_time:.2f}s")
        
        # OPTIMIZATION 2: Smarter text conversion
        excel_text = ""
        total_cells = 0
        non_empty_cells = 0
        
        for sheet_name, df in df_dict.items():
            print(f"Processing sheet '{sheet_name}': {len(df)} rows x {len(df.columns)} cols")
            
            excel_text += f"=== SHEET: {sheet_name} ===\n"
            
            # More intelligent conversion - focus on areas with data
            for idx, row in df.iterrows():
                row_data = []
                has_data = False
                
                for col in df.columns:
                    cell_value = row[col]
                    total_cells += 1
                    
                    if pd.notna(cell_value) and str(cell_value).strip():
                        non_empty_cells += 1
                        has_data = True
                        
                        # Handle Excel dates better
                        if isinstance(cell_value, (int, float)) and cell_value > 40000 and cell_value < 50000:
                            # Likely an Excel date (between 2009-2037)
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
                
                # Only include rows that have actual data
                if has_data:
                    excel_text += f"Row {idx}: " + " | ".join(row_data) + "\n"
            
            excel_text += "\n"
        
        data_density = (non_empty_cells / total_cells * 100) if total_cells > 0 else 0
        print(f"Data density: {data_density:.1f}% ({non_empty_cells}/{total_cells} cells)")
        
        # OPTIMIZATION 3: Use enhanced field mapping service
        schema_prompt = field_mapping_service.create_semantic_schema_prompt()
        
        # OPTIMIZATION 4: Clean up text for Claude
        optimized_text = field_mapping_service.optimize_excel_text_for_claude(excel_text)
        
        # Detect variations for debugging
        detected_variations = field_mapping_service.detect_field_variations(optimized_text)
        variation_summary = field_mapping_service.get_variation_summary(detected_variations)
        print(f"Detected variations: {variation_summary}")
        
        # OPTIMIZATION 5: Limit text size more intelligently
        max_chars = 3500  # Leave room for schema
        if len(optimized_text) > max_chars:
            print(f"Truncating text from {len(optimized_text)} to {max_chars} chars")
            # Try to truncate at a natural break point
            truncated_text = optimized_text[:max_chars]
            last_newline = truncated_text.rfind('\n')
            if last_newline > max_chars * 0.8:  # If we can find a good break point
                optimized_text = truncated_text[:last_newline]
            else:
                optimized_text = truncated_text
        
        print(f"Sending {len(optimized_text)} chars to Claude...")
        
        # Send to Claude with enhanced prompt
        claude_start = time.time()
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2500,  # Increased for more detailed response
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Extract invoice information from this Excel data. Pay special attention to financial totals in the bottom section.
                    
                    {schema_prompt}
                    
                    Excel Data:
                    {optimized_text}
                    """
                }
            ]
        )
        claude_time = time.time() - claude_start
        print(f"Claude processing time: {claude_time:.2f}s")
        
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
            print(f"Total processing time: {total_time:.2f}s")
            
            return jsonify({
                'success': True,
                'data': parsed_data,
                'processing_info': {
                    'detected_variations': detected_variations,
                    'variation_summary': variation_summary,
                    'file_name': file.filename,
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