# services/field_mapping_service.py - ENHANCED VERSION

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
                'created date', 'issued', 'dated', 'date:'
            ],
            'due_date': [
                'due date', 'payment due', 'net due', 'pay by date', 'terms',
                'payment terms', 'due by', 'payable by', 'duedate'
            ],
            'subtotal': [
                'subtotal', 'sub total', 'net amount', 'amount before tax',
                'pre-tax total', 'line total', 'merchandise total'
            ],
            'tax_amount': [
                'tax', 'total tax', 'sales tax', 'vat', 'gst', 'tax amount',
                'taxes', 'state tax', 'local tax', 'hst', 'pst', 'tax due', 'tax '
            ],
            'total_amount': [
                'total', 'grand total', 'amount due', 'TotalDue', 'balance due', 'final amount',
                'total due', 'net total', 'amount owing', 'balance', 'total amount',
                'balance due '  # Added for this specific case
            ],
            # NEW: Additional financial fields
            'freight_amount': [
                'freight', 'shipping', 'shipping cost', 'delivery', 'shipping charge'
            ],
            'discount_amount': [
                'discount', 'additional discount', 'total discount', 'discount applied'
            ]
        }
    
    def create_semantic_schema_prompt(self):
        """Generate enhanced semantic field mapping schema prompt"""
        
        # Build mapping guide text
        mapping_guide = []
        for standard_field, aliases in self.field_aliases.items():
            alias_list = ', '.join(f'"{alias.title()}"' for alias in aliases)
            mapping_guide.append(f'"{standard_field}": Look for any of: [{alias_list}]')
        
        schema_prompt = f"""
        Extract invoice data and return as JSON. Map any field variations to these standard fields:

        FIELD MAPPING GUIDE:
        {chr(10).join(mapping_guide)}

        SPECIAL INSTRUCTIONS:
        1. DATES: If you see numbers like 41585, these are Excel date values - try to interpret them as dates
        2. FINANCIAL LAYOUT: Look for financial totals in the bottom-right area of the invoice
        3. TRAILING SPACES: Field names may have trailing spaces (like "Tax " or "Balance due ")
        4. SCATTERED DATA: Financial summary may be spread across multiple rows, not in a single table
        
        MAPPING RULES:
        1. Always use the exact standard field names in your JSON response
        2. If you find field variations, map them to the standard field
        3. Record the source field name you actually found
        4. Include additional financial fields if found (freight, discount)

        Return JSON with this structure:
        {{
            "vendor_name": "",
            "customer_name": "",
            "invoice_number": "",
            "invoice_date": "",
            "due_date": "",
            "subtotal": 0,
            "tax_amount": 0,
            "freight_amount": 0,
            "discount_amount": 0,
            "total_amount": 0,
            "line_items": [
                {{
                    "description": "",
                    "quantity": 0,
                    "unit_price": 0,
                    "total": 0
                }}
            ],
            "additional_fields": {{
                "po_number": "",
                "ship_date": "",
                "order_date": "",
                "account_number": ""
            }},
            "field_mappings_used": {{
                "tax_source": "actual field name found for tax",
                "total_source": "actual field name found for total",
                "freight_source": "actual field name found for freight (if any)",
                "discount_source": "actual field name found for discount (if any)"
            }},
            "confidence": "high/medium/low"
        }}
        """
        
        return schema_prompt
    
    def detect_field_variations(self, excel_text):
        """Enhanced variation detection with better text cleaning"""
        found_variations = {}
        text_lower = excel_text.lower().strip()
        
        for standard_field, aliases in self.field_aliases.items():
            for alias in aliases:
                alias_lower = alias.lower().strip()
                # More flexible matching - handles trailing spaces and punctuation
                if alias_lower in text_lower or alias_lower.rstrip() in text_lower:
                    if standard_field not in found_variations:
                        found_variations[standard_field] = []
                    if alias not in found_variations[standard_field]:
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
    
    def optimize_excel_text_for_claude(self, excel_text):
        """Clean up Excel text to make it more readable for Claude"""
        
        # Split into lines for processing
        lines = excel_text.split('\n')
        optimized_lines = []
        
        for line in lines:
            # Skip completely empty lines
            if line.strip() == '' or line.strip() == 'None' * 10:
                continue
                
            # Clean up None values and excessive spacing
            cleaned_line = line.replace('None', '').replace('  ', ' ').strip()
            
            # Only keep lines that have actual content
            if cleaned_line and len(cleaned_line) > 2:
                optimized_lines.append(cleaned_line)
        
        return '\n'.join(optimized_lines)