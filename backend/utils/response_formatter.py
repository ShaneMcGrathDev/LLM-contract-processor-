"""
Response formatting utility for API endpoints
"""
from werkzeug.utils import secure_filename

def format_success_response(filename, processing_results):
    """
    Format successful Excel processing response
    
    Args:
        filename: Original filename
        processing_results: Results from excel_processor
        
    Returns:
        dict: Formatted response data
    """
    return {
        'success': True,
        'message': 'Excel file processed and converted to string successfully',
        'filename': secure_filename(filename),
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

def format_error_response(error_type, error_message, troubleshooting_hint=None):
    """
    Format error response
    
    Args:
        error_type: Type of error
        error_message: Error message
        troubleshooting_hint: Optional troubleshooting guidance
        
    Returns:
        dict: Formatted error response
    """
    response = {
        'success': False,
        'error': error_type,
        'message': error_message,
        'troubleshooting': troubleshooting_hint or 'Please check the file and try again'
    }
    
    return response