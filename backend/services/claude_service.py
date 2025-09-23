from anthropic import Anthropic
import os
from dotenv import load_dotenv
import json
import pandas as pd

load_dotenv()

class ClaudeService:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))
        self.model = "claude-3-haiku-20240307"
    
    def analyze_invoice_data(self, data):
        """Analyze invoice data using Claude"""
        try:
            # Handle input data
            if not isinstance(data, dict):
                return {
                    "error": f"Expected dictionary, got {type(data)}",
                    "status": "failed"
                }

            # Clean data by removing nan values and unnamed columns
            cleaned_data = {}
            for k, v in data.items():
                if pd.notna(v) and str(v).strip():
                    # Clean key names and handle special cases
                    key = k
                    if k.startswith('Unnamed:'):
                        continue  # Skip unnamed columns
                    if k == 'INVOICE':
                        key = 'invoice_data'
                    cleaned_data[key] = str(v).strip()

            print(f"Cleaned data for Claude: {cleaned_data}")
            
            if not cleaned_data:
                return {
                    "error": "No valid data found after cleaning",
                    "status": "failed",
                    "original_data": str(data)
                }

            # Construct prompt with example
            prompt = f"""
            Analyze this Excel invoice data and extract key information.
            Data: {cleaned_data}

            Instructions:
            - Company Name appears as 'Company Name' or similar
            - Invoice number might be in the filename or data
            - Look for any monetary values for total amount

            Return ONLY a JSON object in this exact format:
            {{
                "vendor_name": "Company Name",
                "invoice_number": null,
                "total_amount": null
            }}
            """

            message = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Process response
            response_text = message.content[0].text.strip()
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                try:
                    parsed_response = json.loads(json_str)
                    print(f"Successfully parsed response: {parsed_response}")
                    
                    # Ensure all required fields exist
                    for field in ['vendor_name', 'invoice_number', 'total_amount']:
                        if field not in parsed_response:
                            parsed_response[field] = None
                    
                    return parsed_response
                except json.JSONDecodeError as je:
                    print(f"JSON parsing error: {je}")
                    raise
            else:
                raise ValueError("No valid JSON found in Claude's response")
                
        except Exception as e:
            error_msg = f"Claude API Error: {str(e)}"
            print(error_msg)
            return {
                "error": error_msg,
                "status": "failed",
                "model_used": self.model,
                "data_received": str(data)
            }