from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Backend is running!"})

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"data": "Hello from Flask backend!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


