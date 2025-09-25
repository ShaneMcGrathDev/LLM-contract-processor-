# services/database_service.py
from models import db, Invoice
from datetime import datetime
import json

class DatabaseService:
    def __init__(self):
        pass
    
    def save_invoice(self, invoice_data):
        """Save invoice data to database using SQLAlchemy"""
        try:
            # Prepare the processed data (what Claude extracted)
            processed_data = {
                'vendor_name': invoice_data.get('vendor_name'),
                'customer_name': invoice_data.get('customer_name'),
                'invoice_date': invoice_data.get('invoice_date'),
                'due_date': invoice_data.get('due_date'),
                'subtotal': float(invoice_data.get('subtotal', 0)),
                'tax_amount': float(invoice_data.get('tax_amount', 0)),
                'freight_amount': float(invoice_data.get('freight_amount', 0)),
                'discount_amount': float(invoice_data.get('discount_amount', 0)),
                'total_amount': float(invoice_data.get('total_amount', 0)),
                'line_items': invoice_data.get('line_items', []),
                'confidence': invoice_data.get('confidence'),
                'field_mappings_used': invoice_data.get('field_mappings_used', {})
            }
            
            # Create new invoice record
            invoice = Invoice(
                vendor_name=invoice_data.get('vendor_name', 'Unknown Vendor'),
                invoice_number=invoice_data.get('invoice_number', 'N/A'),
                total_amount=float(invoice_data.get('total_amount', 0)),
                raw_data=invoice_data,  # Store the complete raw data from Claude
                processed_data=processed_data,  # Store the structured processed data
                status='processed'  # Set status as processed
            )
            
            # Add to session and commit
            db.session.add(invoice)
            db.session.commit()
            
            print(f"Invoice saved successfully with ID: {invoice.id}")
            
            return {
                'success': True,
                'message': 'Invoice saved successfully',
                'invoice_id': invoice.id,
                'data': invoice.to_dict()
            }
            
        except Exception as e:
            # Rollback in case of error
            db.session.rollback()
            print(f"Database save error: {str(e)}")
            
            return {
                'success': False,
                'message': f'Database error: {str(e)}'
            }
    
    def get_invoice(self, invoice_id):
        """Retrieve a specific invoice by ID"""
        try:
            invoice = Invoice.query.get(invoice_id)
            
            if not invoice:
                return {
                    'success': False, 
                    'message': 'Invoice not found'
                }
            
            return {
                'success': True,
                'data': invoice.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Database error: {str(e)}'
            }
    
    def get_all_invoices(self, limit=50, offset=0):
        """Get all invoices with pagination"""
        try:
            # Query with pagination
            invoices_query = Invoice.query.order_by(Invoice.created_at.desc())
            
            # Get total count for pagination info
            total_count = invoices_query.count()
            
            # Apply pagination
            invoices = invoices_query.offset(offset).limit(limit).all()
            
            # Convert to dictionaries
            invoice_list = [invoice.to_dict() for invoice in invoices]
            
            return {
                'success': True,
                'data': invoice_list,
                'total_count': total_count,
                'pagination': {
                    'limit': limit,
                    'offset': offset,
                    'total_pages': (total_count + limit - 1) // limit,
                    'current_page': (offset // limit) + 1
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Database error: {str(e)}'
            }
    
    def update_invoice(self, invoice_id, invoice_data):
        """Update an existing invoice"""
        try:
            invoice = Invoice.query.get(invoice_id)
            
            if not invoice:
                return {
                    'success': False,
                    'message': 'Invoice not found'
                }
            
            # Update the fields
            invoice.vendor_name = invoice_data.get('vendor_name', invoice.vendor_name)
            invoice.invoice_number = invoice_data.get('invoice_number', invoice.invoice_number)
            invoice.total_amount = float(invoice_data.get('total_amount', invoice.total_amount))
            
            # Update processed_data with new values
            updated_processed_data = {
                'vendor_name': invoice_data.get('vendor_name'),
                'customer_name': invoice_data.get('customer_name'),
                'invoice_date': invoice_data.get('invoice_date'),
                'due_date': invoice_data.get('due_date'),
                'subtotal': float(invoice_data.get('subtotal', 0)),
                'tax_amount': float(invoice_data.get('tax_amount', 0)),
                'freight_amount': float(invoice_data.get('freight_amount', 0)),
                'discount_amount': float(invoice_data.get('discount_amount', 0)),
                'total_amount': float(invoice_data.get('total_amount', 0)),
                'line_items': invoice_data.get('line_items', []),
                'confidence': invoice_data.get('confidence'),
                'field_mappings_used': invoice_data.get('field_mappings_used', {})
            }
            
            invoice.processed_data = updated_processed_data
            invoice.updated_at = datetime.utcnow()
            invoice.status = 'updated'
            
            # Commit changes
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Invoice updated successfully',
                'data': invoice.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Database error: {str(e)}'
            }
    
    def delete_invoice(self, invoice_id):
        """Delete an invoice"""
        try:
            invoice = Invoice.query.get(invoice_id)
            
            if not invoice:
                return {
                    'success': False,
                    'message': 'Invoice not found'
                }
            
            db.session.delete(invoice)
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Invoice deleted successfully'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Database error: {str(e)}'
            }
    
    def get_invoices_by_vendor(self, vendor_name, limit=20):
        """Get invoices by vendor name"""
        try:
            invoices = Invoice.query.filter(
                Invoice.vendor_name.ilike(f'%{vendor_name}%')
            ).order_by(Invoice.created_at.desc()).limit(limit).all()
            
            return {
                'success': True,
                'data': [invoice.to_dict() for invoice in invoices]
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Database error: {str(e)}'
            }