from flask import Blueprint, jsonify, request
import pandas as pd
from services.claude_service import ClaudeService
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()

# Initialize Claude service
claude_service = ClaudeService()

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Configuration
ALLOWED_EXTENSIONS = {'.xlsx', '.xls'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_file(file):
    """Validate uploaded Excel file"""
    if not file:
        return False, "No file included in request", "Please include a file in the request"
    
    if file.filename == '':
        return False, "No file selected", "File field is empty"
    
    # Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        return False, "Invalid file type", f"Please upload Excel files (.xlsx or .xls) only. Received: {file_ext}"
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset file pointer
    
    if file_size > MAX_FILE_SIZE:
        return False, "File too large", f"File size ({file_size / (1024*1024):.1f}MB) exceeds limit ({MAX_FILE_SIZE / (1024*1024)}MB)"
    
    if file_size == 0:
        return False, "Empty file", "The uploaded file is empty"
    
    return True, "Valid file", None

def process_excel_to_string(file):
    """Process Excel file and convert to string representation"""
    try:
        # Read Excel file - handle multiple sheets
        excel_file = pd.ExcelFile(file)
        
        processing_results = {
            'sheet_names': excel_file.sheet_names,
            'sheet_count': len(excel_file.sheet_names),
            'sheets_data': {},
            'claude_ready_string': ""
        }
        
        combined_text_parts = []
        
        # Process each sheet
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file, sheet_name=sheet_name)
            
            # Debug prints (as in your original code)
            print(f"\n=== Sheet: {sheet_name} ===")
            print(f"DataFrame head: {df.head()}")
            print(f"DataFrame info: {df.info()}")
            print(f"DataFrame columns: {df.columns.tolist()}")
            print(f"DataFrame dtypes: {df.dtypes}")
            print(f"DataFrame shape: {df.shape}")
            print(f"DataFrame description: {df.describe(include='all')}")
            print(f"DataFrame Overall: {df}")
            
            # Convert to string representation
            sheet_string = df.to_string()
            
            # Store sheet analysis
            sheet_data = {
                'shape': {
                    'rows': int(df.shape[0]),
                    'columns': int(df.shape[1])
                },
                'columns': df.columns.tolist(),
                'data_types': df.dtypes.astype(str).to_dict(),
                'has_null_values': bool(df.isnull().sum().sum() > 0),
                'null_counts': {k: int(v) for k, v in df.isnull().sum().to_dict().items()},
                'sample_data': df.head(5).fillna('').to_dict('records'),
                'string_representation': sheet_string
            }
            
            processing_results['sheets_data'][sheet_name] = sheet_data
            
            # Add to combined string for Claude
            if len(excel_file.sheet_names) > 1:
                combined_text_parts.append(f"--- Sheet: {sheet_name} ---\n{sheet_string}")
            else:
                combined_text_parts.append(sheet_string)
        
        # Create combined string for Claude processing
        processing_results['claude_ready_string'] = "\n\n".join(combined_text_parts)
        
        print(f"\n=== CLAUDE READY STRING LENGTH: {len(processing_results['claude_ready_string'])} characters ===")
        print("Preview (first 300 characters):")
        print(processing_results['claude_ready_string'][:300])
        print("..." if len(processing_results['claude_ready_string']) > 300 else "")
        
        return processing_results
        
    except Exception as e:
        raise Exception(f"Excel processing error: {str(e)}")

@api_bp.route('/upload-excel', methods=['POST'])
def check_excel_load():
    try:
        # Step 1: Validate file
        file = request.files.get('file')
        is_valid, error_type, error_message = validate_file(file)
        
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_type,
                'message': error_message,
                'troubleshooting': 'Please check the file and try again'
            }), 400
        
        # Step 2: Process Excel file to string
        processing_results = process_excel_to_string(file)
        
        # Step 3: Prepare response with both detailed analysis and Claude-ready string
        response_data = {
            'success': True,
            'message': 'Excel file processed and converted to string successfully',
            'filename': secure_filename(file.filename),
            'file_analysis': {
                'sheet_count': processing_results['sheet_count'],
                'sheet_names': processing_results['sheet_names'],
                'claude_string_length': len(processing_results['claude_ready_string']),
                'sheets_summary': {
                    name: {
                        'rows': data['shape']['rows'],
                        'columns': data['shape']['columns'],
                        'has_nulls': data['has_null_values']
                    }
                    for name, data in processing_results['sheets_data'].items()
                }
            },
            'detailed_analysis': processing_results['sheets_data'],
            'claude_ready_string': processing_results['claude_ready_string'],
            'status': 'Ready for Claude processing'
        }
        
        # Future Claude integration point (commented out for now)
        # claude_response = claude_service.analyze_invoice_data(processing_results['claude_ready_string'])
        # response_data['claude_response'] = claude_response
        
        return jsonify(response_data), 200
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'File processing failed',
            'message': str(e),
            'troubleshooting': 'Ensure the Excel file is valid and not corrupted'
        }), 500