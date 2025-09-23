"""
File validation utility for Excel uploads
"""
import os

# Configuration
ALLOWED_EXTENSIONS = {'.xlsx', '.xls'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_file(file):
    """
    Validate uploaded Excel file
    
    Args:
        file: Flask uploaded file object
        
    Returns:
        tuple: (is_valid: bool, error_type: str, error_message: str)
    """
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