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
    


class Invoice(db.Model):
    __tablename__ = 'invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    vendor_name = db.Column(db.String(255), nullable=False)
    invoice_number = db.Column(db.String(255), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    raw_data = db.Column(db.JSON)
    processed_data = db.Column(db.JSON)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'vendor_name': self.vendor_name,
            'invoice_number': self.invoice_number,
            'total_amount': self.total_amount,
            'raw_data': self.raw_data,
            'processed_data': self.processed_data,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }