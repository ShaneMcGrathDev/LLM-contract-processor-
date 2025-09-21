import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Create the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Generate content
response = model.generate_content("Provide 3 benefits of using AI in the Medical Device industry for contracts")
print(response.text)