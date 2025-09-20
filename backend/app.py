from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Debug: Check if environment variables are loaded
print("DATABASE_URL:", os.getenv('DATABASE_URL'))
print("Current working directory:", os.getcwd())
print("Files in current directory:", os.listdir('.'))

# Database configuration
database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set!")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Backend is running!"})

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"data": "Hello from Flask backend!"})

@app.route('/api/test-db', methods=['GET'])
def test_database():
    try:
        # Test the connection
        result = db.session.execute(text("SELECT 1"))
        return jsonify({"status": "success", "message": "Database connected!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)