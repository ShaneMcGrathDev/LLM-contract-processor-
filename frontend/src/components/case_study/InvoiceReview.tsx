import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Paper } from '@mui/material';

interface InvoiceData {
    vendor_name: string;
    invoice_number: string;
    total_amount: number;
    raw_data: any;
    processed_data: any;
    status: string;
}

const InvoiceReview: React.FC<{
    invoiceData: InvoiceData;
    onSubmit: (data: InvoiceData) => void;
}> = ({ invoiceData, onSubmit }) => {
    const [editedData, setEditedData] = useState<InvoiceData>(invoiceData);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit(editedData);
    };

    return (
        <Paper elevation={3} sx={{ p: 3, my: 2 }}>
            <Typography variant="h6" gutterBottom>
                Review Invoice Data
            </Typography>
            <form onSubmit={handleSubmit}>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <TextField
                        label="Vendor Name"
                        value={editedData.vendor_name}
                        onChange={(e) => setEditedData({
                            ...editedData,
                            vendor_name: e.target.value
                        })}
                    />
                    <TextField
                        label="Invoice Number"
                        value={editedData.invoice_number}
                        onChange={(e) => setEditedData({
                            ...editedData,
                            invoice_number: e.target.value
                        })}
                    />
                    <TextField
                        label="Total Amount"
                        type="number"
                        value={editedData.total_amount}
                        onChange={(e) => setEditedData({
                            ...editedData,
                            total_amount: parseFloat(e.target.value)
                        })}
                    />
                    <Button
                        type="submit"
                        variant="contained"
                        color="primary"
                    >
                        Submit Invoice
                    </Button>
                </Box>
            </form>
        </Paper>
    );
};

export default InvoiceReview;