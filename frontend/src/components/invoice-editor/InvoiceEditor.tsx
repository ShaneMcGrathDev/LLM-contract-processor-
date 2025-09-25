'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { useRouter } from 'next/navigation';
import { Eye } from 'lucide-react';

export default function InvoiceEditor({ data }) {
    const [formData, setFormData] = useState(data);
    const [saving, setSaving] = useState(false);
    const router = useRouter();

    const handleSubmit = async () => {
        setSaving(true);
        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/review-invoice`, {
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

    const handleViewDetails = () => {
        console.log('🔍 Debug: Form data being stored:', formData);

        try {
            // Store data in localStorage
            localStorage.setItem('currentInvoiceData', JSON.stringify(formData));

            // Verify it was stored
            const storedData = localStorage.getItem('currentInvoiceData');
            console.log('✅ Data stored successfully:', storedData ? 'Yes' : 'No');
            console.log('📄 Stored data preview:', storedData?.substring(0, 100) + '...');

            router.push('/invoice-data');
        } catch (error) {
            console.error('❌ Error storing data:', error);
            alert('Error storing invoice data. Check console.');
        }
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
                    <label className="block text-sm font-medium mb-1">Subtotal</label>
                    <input
                        type="number"
                        step="0.01"
                        value={formData.subtotal || 0}
                        onChange={(e) => updateField('subtotal', parseFloat(e.target.value) || 0)}
                        className="w-full p-2 border rounded"
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium mb-1">Tax Amount</label>
                    <input
                        type="number"
                        step="0.01"
                        value={formData.tax_amount || 0}
                        onChange={(e) => updateField('tax_amount', parseFloat(e.target.value) || 0)}
                        className="w-full p-2 border rounded"
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium mb-1">Freight Amount</label>
                    <input
                        type="number"
                        step="0.01"
                        value={formData.freight_amount || 0}
                        onChange={(e) => updateField('freight_amount', parseFloat(e.target.value) || 0)}
                        className="w-full p-2 border rounded"
                    />
                </div>

                <div className="md:col-span-2">
                    <label className="block text-sm font-medium mb-1">Total Amount</label>
                    <input
                        type="number"
                        step="0.01"
                        value={formData.total_amount || 0}
                        onChange={(e) => updateField('total_amount', parseFloat(e.target.value) || 0)}
                        className="w-full p-2 border rounded bg-green-50 border-green-200 font-semibold"
                    />
                </div>
            </div>

            <div className="flex gap-3">
                <Button
                    onClick={handleViewDetails}
                    variant="outline"
                    size="sm"
                    className="transition-all duration-200 hover:scale-105 hover:shadow-md"
                >
                    <Eye className="h-4 w-4 mr-2" />
                    More Details
                </Button>

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
        </div>
    );
}