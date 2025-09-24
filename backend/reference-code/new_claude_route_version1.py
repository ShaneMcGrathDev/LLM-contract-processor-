
####This is the working route prior to adding the field_mapping service to handle non-standard field cases during invoice submissions

###Keeping this here for now in case I need to revert back to it



# Updated claude_test route with API key debugging



# @api_bp.route('/claude_test', methods=['POST'])
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