from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class NumberSubmission(db.Model):
    __tablename__ = 'number_submissions'
    
    # Columns in your database table
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    doubled = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Helper method to convert to dictionary (for JSON responses)
    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'doubled': self.doubled,
            'created_at': self.created_at.isoformat()
        }