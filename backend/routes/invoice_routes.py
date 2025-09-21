# from flask import Blueprint, jsonify, request
# from services.invoice_processor import InvoiceProcessor
# from services.data_service import DataService

# # Create blueprint for invoice processing
# invoice_bp = Blueprint('invoice', __name__, url_prefix='/api/invoices')

# @invoice_bp.route('/upload', methods=['POST'])
# def upload_invoice():
#     # Future: Handle file upload and LLM processing
#     return jsonify({"message": "Invoice processing endpoint - coming soon!"})

# @invoice_bp.route('/extract', methods=['POST'])
# def extract_data():
#     # Future: Extract data from invoice using LLM
#     return jsonify({"message": "Data extraction endpoint - coming soon!"})

# @invoice_bp.route('/processed', methods=['GET'])
# def get_processed_invoices():
#     # Future: Get all processed invoices
#     return jsonify({"message": "Processed invoices endpoint - coming soon!"})