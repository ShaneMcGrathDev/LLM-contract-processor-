#database_service.py

from models import db, Invoice

class DatabaseService:
    """Database operations for invoice processing"""
    
    def __init__(self):
        self.db = db
    
    def save_invoice(self, invoice_data):
        """Save processed and reviewed invoice data"""
        try:
            invoice = Invoice(
                vendor_name=invoice_data.get('vendor_name'),
                invoice_number=invoice_data.get('invoice_number'),
                total_amount=invoice_data.get('total_amount'),
                raw_data=invoice_data.get('raw_data'),
                processed_data=invoice_data.get('processed_data'),
                status='reviewed'
            )
            
            self.db.session.add(invoice)
            self.db.session.commit()
            
            return {
                'success': True,
                'invoice_id': invoice.id,
                'message': 'Invoice saved successfully'
            }
            
        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Database error: {str(e)}")