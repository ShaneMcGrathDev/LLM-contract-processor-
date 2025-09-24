
# excel_processor.py


"""
Multi-sheet Excel file processing routine 
"""
import pandas as pd

def process_excel_to_string(file):
    """
    Process Excel file and convert to string representation for Claude processing
    
    Args:
        file: Flask uploaded file object
        
    Returns:
        dict: Processing results including string representation and analysis data
        
    Raises:
        Exception: If Excel processing fails
    """

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
        
        # Process each sheet, each sheet becomes a dataframe
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file, sheet_name=sheet_name)
            
            # Debug prints for development
            print(f"\n=== Sheet: {sheet_name} ===")
            print(f"DataFrame head: {df.head()}")
            print(f"DataFrame info: {df.info()}")
            print(f"DataFrame columns: {df.columns.tolist()}")
            print(f"DataFrame dtypes: {df.dtypes}")
            print(f"DataFrame shape: {df.shape}")
            print(f"DataFrame description: {df.describe(include='all')}")
            print(f"DataFrame Overview: {df}")
            
            # Convert to string representation
            sheet_string = df.to_string()
            
            # Store detailed sheet analysis
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
            
            # This is the sheets nested dictionary. 
            # Builds another key called sheet_name set to the 
            processing_results['sheets_data'][sheet_name] = sheet_data
            
            # Add to combined string for Claude
            if len(excel_file.sheet_names) > 1:
                combined_text_parts.append(f"--- Sheet: {sheet_name} ---\n{sheet_string}")
            else:
                combined_text_parts.append(sheet_string)
        
        # Create combined string for Claude processing
        processing_results['claude_ready_string'] = "\n\n".join(combined_text_parts)
        
        # Log string info for debugging
        print(f"\n=== CLAUDE READY STRING ===")
        print(f"Length: {len(processing_results['claude_ready_string'])} characters")
        print("Preview (first 300 characters):")
        print(processing_results['claude_ready_string'][:300])
        print("..." if len(processing_results['claude_ready_string']) > 300 else "")
        
        return processing_results
        
    except Exception as e:
        raise Exception(f"Excel processing error: {str(e)}")