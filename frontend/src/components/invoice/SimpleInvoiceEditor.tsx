'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';

export default function SimpleInvoiceEditor({ data }) {
    const [formData, setFormData] = useState(data);
    const [saving, setSaving] = useState(false);

    const handleSubmit = async () => {
        setSaving(true);
        try {
            const res = await fetch('http://localhost:5000/api/review-invoice', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ invoice_data: formData }),
            });
            if (res.ok) {
                alert('Invoice saved successfully!');
            }
        } catch (error) {
            alert('Save failed');
        }
        setSaving(false);
    };

    const updateField = (field, value) => {
        setFormData(prev => ({ ...prev, [field]: value }));
    };

    return (
        <div className="p-4 border rounded-lg shadow-sm space-y-4">
            <h3 className="text-lg font-medium">Edit Invoice Data</h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium mb-1">Vendor Name</label>
                    <input
                        type="text"
                        value={formData.vendor_name || ''}
                        onChange={(e) => updateField('vendor_name', e.target.value)}
                        className="w-full p-2 border rounded"
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium mb-1">Invoice Number</label>
                    <input
                        type="text"
                        value={formData.invoice_number || ''}
                        onChange={(e) => updateField('invoice_number', e.target.value)}
                        className="w-full p-2 border rounded"
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium mb-1">Total Amount</label>
                    <input
                        type="number"
                        value={formData.total_amount || 0}
                        onChange={(e) => updateField('total_amount', parseFloat(e.target.value) || 0)}
                        className="w-full p-2 border rounded"
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium mb-1">Tax Amount</label>
                    <input
                        type="number"
                        value={formData.tax_amount || 0}
                        onChange={(e) => updateField('tax_amount', parseFloat(e.target.value) || 0)}
                        className="w-full p-2 border rounded"
                    />
                </div>
            </div>

            <Button
                onClick={handleSubmit}
                disabled={saving}
                variant="default"
                size="default"
                className="transition-all duration-200 hover:scale-105 hover:shadow-md"
            >
                {saving ? 'Saving...' : 'Save to Database'}
            </Button>
        </div>
    );
}