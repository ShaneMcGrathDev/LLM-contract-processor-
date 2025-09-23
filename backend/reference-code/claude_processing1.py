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




# @api_bp.route('/upload-excel', methods=['POST'])
# def check_excel_load():
#     try:
#         if 'file' not in request.files:
#             return jsonify({'error': 'No file included in request'}), 400
            
#         file = request.files['file']
        
#         # Read Excel file into pandas DataFrame
#         df = pd.read_excel(file)
        
#         # Convert first row to JSON for Claude processing
#         first_row = df.iloc[0].to_json()
        
#         # Get Claude response
#         response = claude_service.analyze_invoice_data(first_row)
        
#         return jsonify({
#             'message': 'File processed successfully',
#             'filename': file.filename,
#             'claude_response': response,
#             'row_data': first_row
#         }), 200
            
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    
@api_bp.route('/upload-excel', methods=['POST'])
def check_excel_load():
    try:
        # Add debug logging
        print("Starting file upload process...")
        
        if 'file' not in request.files:
            print("No file found in request")
            return jsonify({'error': 'No file included in request'}), 400
            
        file = request.files['file']
        print(f"Received file: {file.filename}")
        
        if file.filename == '':
            print("Empty filename received")
            return jsonify({'error': 'No file selected'}), 400
        
        # Log file type
        print(f"File type: {file.content_type}")
        
        if not file.filename.lower().endswith(('.xlsx', '.xls')):
            print(f"Invalid file type: {file.filename}")
            return jsonify({'error': 'File must be an Excel file (.xlsx or .xls)'}), 400
        
        try:
            # Read Excel file with explicit error handling
            df = pd.read_excel(file)
            print(f"Successfully read Excel file with {len(df)} rows")
            print(df)
            
        except Exception as excel_error:
            print(f"Excel reading error: {str(excel_error)}")
            return jsonify({'error': f'Failed to read Excel file: {str(excel_error)}'}), 400
        
        if df.empty:
            print("DataFrame is empty")
            return jsonify({'error': 'Excel file is empty'}), 400
        
        # Convert first row to dict and log it
        first_row = df.iloc[0].to_dict()
        print(f"First row data: {first_row}")
        
        # Get Claude response with error handling
        try:
            claude_response = claude_service.analyze_invoice_data(str(first_row))
            print("Claude analysis completed")
            
        except Exception as claude_error:
            print(f"Claude analysis error: {str(claude_error)}")
            return jsonify({'error': f'Claude analysis failed: {str(claude_error)}'}), 500
        
        return jsonify({
            'message': 'File processed successfully',
            'filename': file.filename,
            'rows_processed': len(df),
            'columns': list(df.columns),
            'claude_analysis': claude_response,
            'sample_data': first_row
        }), 200
            
    except Exception as e:
        print(f"Unexpected error in upload-excel route: {str(e)}")
        return jsonify({'error': str(e)}), 500