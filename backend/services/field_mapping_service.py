# Enhanced schema with semantic field mapping
def field_mapping_service():
    schema_prompt = """
    Extract invoice data and return as JSON. Map any variations to these standard fields:

    FIELD MAPPING GUIDE:
    "vendor_name": Look for any of: [Company Name, Vendor, Supplier, From, Seller, Bill From, Service Provider]
    "customer_name": Look for any of: [Customer, Sold To, Bill To, Client, Buyer, Ship To, Account Name]
    "invoice_number": Look for any of: [Invoice #, Invoice Number, Inv #, Reference, Document Number, Bill #]
    "invoice_date": Look for any of: [Invoice Date, Date, Issue Date, Bill Date, Document Date]
    "due_date": Look for any of: [Due Date, Payment Due, Net Due, Pay By Date, Terms]
    "subtotal": Look for any of: [Subtotal, Sub Total, Net Amount, Amount Before Tax, Pre-Tax Total]
    "tax_amount": Look for any of: [Tax, Total Tax, Sales Tax, VAT, GST, Tax Amount, Taxes]
    "total_amount": Look for any of: [Total, Grand Total, Amount Due, Final Amount, Balance Due, Total Due]

    IMPORTANT: Always map field variations to the standard field names above.
    If you find "Sales Tax", map it to "tax_amount".
    If you find "Sold To", map it to "customer_name".

    Return JSON with this exact structure:
    {
        "vendor_name": "",
        "customer_name": "",
        "invoice_number": "",
        "invoice_date": "",
        "due_date": "",
        "subtotal": 0,
        "tax_amount": 0,
        "total_amount": 0,
        "line_items": [
            {
                "description": "",
                "quantity": 0,
                "unit_price": 0,
                "total": 0
            }
        ],
        "field_mappings_used": {
            "tax_source": "what field name was actually found for tax",
            "customer_source": "what field name was actually found for customer"
        },
        "confidence": "high/medium/low"
    }
    """
    return schema_prompt