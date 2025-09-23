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
            return jsonify({
                'success': False,
                'error': 'No file included in request',
                'message': 'Please include a file in the request'
            }), 400
            
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected',
                'message': 'File field is empty'
            }), 400
        
        # Validate file type
        if not file.filename.lower().endswith(('.xlsx', '.xls')):
            return jsonify({
                'success': False,
                'error': 'Invalid file type',
                'message': 'Please upload Excel files (.xlsx or .xls) only'
            }), 400
        
        # Read Excel file into pandas DataFrame
        df = pd.read_excel(file)
        
        # Print examination data to console for debugging
        print(f"DataFrame head: {df.head()}")
        print(f"DataFrame info: {df.info()}")
        print(f"DataFrame columns: {df.columns.tolist()}")
        print(f"DataFrame dtypes: {df.dtypes}")
        print(f"DataFrame shape: {df.shape}")
        print(f"DataFrame description: {df.describe(include='all')}")
        print(f"DataFrame Overall: {df}")
        
        # Prepare examination results for response
        examination_data = {
            'shape': {
                'rows': int(df.shape[0]),
                'columns': int(df.shape[1])
            },
            'columns': df.columns.tolist(),
            'data_types': df.dtypes.astype(str).to_dict(),
            'has_null_values': bool(df.isnull().sum().sum() > 0),
            'null_counts': df.isnull().sum().to_dict(),
            'sample_data': df.head(5).fillna('').to_dict('records'),
            'string_representation': df.to_string()
        }
        
        # Convert first row to JSON (commented out for now as requested)
        # first_row = df.iloc[0].to_json()
        
        # Get Claude response (commented out for now as requested)
        # response = claude_service.analyze_invoice_data(first_row)
        
        return jsonify({
            'success': True,
            'message': 'Excel file processed and examined successfully',
            'filename': file.filename,
            'file_analysis': examination_data,
            'status': 'Ready for Claude processing'
            # 'claude_response': response,
            # 'row_data': first_row
        }), 200
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'File processing failed',
            'message': str(e),
            'troubleshooting': 'Ensure the Excel file is valid and not corrupted'
        }), 500