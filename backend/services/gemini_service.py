import google.generativeai as genai
import os
from PIL import Image
import json

class GeminiService:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro-vision')
    
    def extract_invoice_data(self, image_path):
        """Extract structured data from invoice image"""
        try:
            # Open the image
            image = Image.open(image_path)
            
            # Craft a prompt for structured extraction
            prompt = """
            Analyze this invoice image and extract the following information in JSON format:
            {
                "vendor_name": "company name",
                "invoice_number": "invoice number",
                "date": "invoice date",
                "total_amount": "total amount as number",
                "currency": "currency symbol or code",
                "items": [
                    {
                        "description": "item description",
                        "quantity": "quantity as number",
                        "unit_price": "price as number",
                        "total": "line total as number"
                    }
                ]
            }
            
            Return only valid JSON. If any field cannot be found, use null.
            """
            
            # Send to Gemini
            response = self.model.generate_content([prompt, image])
            
            # Parse the JSON response
            json_data = json.loads(response.text)
            
            return {
                "success": True,
                "data": json_data,
                "raw_response": response.text
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }