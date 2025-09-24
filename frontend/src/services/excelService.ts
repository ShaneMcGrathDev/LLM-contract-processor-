import { ExcelUploadResponse, InvoiceData } from '../types/excelTypes';

const API_BASE_URL = 'http://localhost:5000/api';

export const uploadExcel = async (file: File): Promise<ExcelUploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/upload-excel`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        throw new Error('Failed to upload file');
    }

    return response.json();
};

export const submitInvoice = async (invoiceData: InvoiceData) => {
    const response = await fetch(`${API_BASE_URL}/review-invoice`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ invoice_data: invoiceData })
    });

    if (!response.ok) {
        throw new Error('Failed to submit invoice');
    }

    return response.json();
};