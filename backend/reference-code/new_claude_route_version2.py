
###Second version of Claude route with form field variation handling
# This works but running a little slow and missing some fields
# will update corresponding service to handle fields better and add new ones

#Going to develop further to optimize for speed and capture additional invoice metadata correctly

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
        print("Claude client initialized")
        
        # Get the uploaded file
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        print(f"File received: {file.filename}")
        
        # Read Excel file
        df = pd.read_excel(file, sheet_name=None)
        print(f"Excel sheets: {list(df.keys())}")
        
        # Convert to text format for Claude
        excel_text = ""
        for sheet_name, sheet_df in df.items():
            excel_text += f"=== SHEET: {sheet_name} ===\n"
            excel_text += sheet_df.to_string(index=False, na_rep='')
            excel_text += "\n\n"
        
        print(f"Excel text length: {len(excel_text)}")
        
        # NEW: Use field mapping service to create semantic schema
        schema_prompt = field_mapping_service.create_semantic_schema_prompt()
        
        # NEW: Detect field variations for debugging/logging
        detected_variations = field_mapping_service.detect_field_variations(excel_text)
        variation_summary = field_mapping_service.get_variation_summary(detected_variations)
        print(f"Detected field variations: {variation_summary}")
        
        print("Sending request to Claude...")
        
        # Send to Claude with semantic mapping schema
        #This is the Anthropic API structure 
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Please extract invoice information from this Excel data using the semantic field mapping rules provided.
                    
                    {schema_prompt}
                    
                    Excel Data:
                    {excel_text[:4000]}
                    """
                }
            ]
        )
        
        print("Received response from Claude")
        response_text = message.content[0].text
        print(f"Claude response length: {len(response_text)}")
        
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
            print("Successfully parsed JSON from Claude")
            
            return jsonify({
                'success': True,
                'data': parsed_data,
                'processing_info': {
                    'detected_variations': detected_variations,
                    'variation_summary': variation_summary,
                    'file_name': file.filename
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