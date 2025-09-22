from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

class ClaudeService:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))
    
    def analyze_invoice_data(self, data):
        try:
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": f"""
                    Analyze this invoice data and extract these fields:
                    - Vendor Name
                    - Invoice Number
                    - Total Amount
                    
                    Data: {data}
                    
                    Return only JSON format.
                    """
                }]
            )
            return message.content
            
        except Exception as e:
            return {"error": str(e)}