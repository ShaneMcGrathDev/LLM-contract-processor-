export interface ExcelUploadResponse {
    message?: string;
    filename?: string;
    error?: string;
    claude_analysis?: {
        vendor_name: string;
        invoice_number: string;
        total_amount: number;
        raw_data: any;
        processed_data: any;
    };
}

export interface InvoiceData {
    vendor_name: string;
    invoice_number: string;
    total_amount: number;
    raw_data: any;
    processed_data: any;
}