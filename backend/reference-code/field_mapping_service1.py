
#This is the field mapping service version 1
# Version 2 adds a few more field variation case and adds the tax field, etc.

# services/field_mapping_service.py

class FieldMappingService:
    def __init__(self):
        self.field_aliases = {
            'vendor_name': [
                'vendor', 'supplier', 'company', 'from', 'seller', 'service provider',
                'bill from', 'remit to', 'company name', 'business name', 'contractor'
            ],
            'customer_name': [
                'customer', 'sold to', 'bill to', 'ship to', 'client', 'buyer',
                'account', 'customer name', 'client name', 'account name', 'recipient'
            ],
            'invoice_number': [
                'invoice', 'invoice #', 'inv #', 'invoice number', 'reference',
                'document number', 'bill #', 'bill number', 'ref #', 'po number'
            ],
            'invoice_date': [
                'invoice date', 'date', 'issue date', 'bill date', 'document date',
                'created date', 'issued', 'dated'
            ],
            'due_date': [
                'due date', 'payment due', 'net due', 'pay by date', 'terms',
                'payment terms', 'due by', 'payable by'
            ],
            'subtotal': [
                'subtotal', 'sub total', 'net amount', 'amount before tax',
                'pre-tax total', 'line total', 'merchandise total'
            ],
            'tax_amount': [
                'tax', 'total tax', 'sales tax', 'vat', 'gst', 'tax amount',
                'taxes', 'state tax', 'local tax', 'hst', 'pst', 'tax due'
            ],
            'total_amount': [
                'total', 'grand total', 'amount due', 'balance due', 'final amount',
                'total due', 'net total', 'amount owing', 'balance', 'total amount'
            ]
        }
    
    def create_semantic_schema_prompt(self):
        """Generate the semantic field mapping schema prompt"""
        
        # Build mapping guide text
        mapping_guide = []
        for standard_field, aliases in self.field_aliases.items():
            alias_list = ', '.join(f'"{alias.title()}"' for alias in aliases)
            mapping_guide.append(f'"{standard_field}": Look for any of: [{alias_list}]')
        
        schema_prompt = f"""
        Extract invoice data and return as JSON. Map any field variations to these standard fields:

        FIELD MAPPING GUIDE:
        {chr(10).join(mapping_guide)}

        MAPPING RULES:
        1. Always use the exact standard field names in your JSON response
        2. If you find field variations (like "Sales Tax"), map them to the standard field ("tax_amount")
        3. Record what source field you actually found in the "field_mappings_used" section
        4. If multiple variations exist for the same field, choose the most complete/official one

        Return JSON with this exact structure:
        {{
            "vendor_name": "",
            "customer_name": "",
            "invoice_number": "",
            "invoice_date": "",
            "due_date": "",
            "subtotal": 0,
            "tax_amount": 0,
            "total_amount": 0,
            "line_items": [
                {{
                    "description": "",
                    "quantity": 0,
                    "unit_price": 0,
                    "total": 0
                }}
            ],
            "field_mappings_used": {{
                "tax_source": "actual field name found for tax (e.g., 'Sales Tax')",
                "customer_source": "actual field name found for customer (e.g., 'Sold To')",
                "vendor_source": "actual field name found for vendor",
                "total_source": "actual field name found for total amount"
            }},
            "confidence": "high/medium/low"
        }}
        """
        
        return schema_prompt
    
    def detect_field_variations(self, excel_text):
        """Analyze text to identify which field variations are present"""
        found_variations = {}
        text_lower = excel_text.lower()
        
        for standard_field, aliases in self.field_aliases.items():
            for alias in aliases:
                if alias.lower() in text_lower:
                    if standard_field not in found_variations:
                        found_variations[standard_field] = []
                    found_variations[standard_field].append(alias)
        
        return found_variations
    
    def get_variation_summary(self, detected_variations):
        """Create a summary of detected variations for logging/debugging"""
        if not detected_variations:
            return "No field variations detected"
        
        summary = []
        for field, variations in detected_variations.items():
            summary.append(f"{field}: {', '.join(variations)}")
        
        return "; ".join(summary)