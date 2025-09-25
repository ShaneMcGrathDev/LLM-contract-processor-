'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';

export default function InvoiceProcessor({ onDataReceived }) {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleUpload = async () => {
        if (!file) return;
        setLoading(true);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const res = await fetch('http://localhost:5000/api/claude_test', {
                method: 'POST',
                body: formData,
            });
            const response = await res.json();
            if (response.success) {
                onDataReceived(response.data);
                toast.success("Invoice processed successfully! You can now edit the fields below.");
            } else {
                toast.error("Failed to process invoice. Please try again.");
            }
        } catch (error) {
            console.error('Upload failed:', error);
            toast.error("Upload failed. Please check your connection and try again.");
        }
        setLoading(false);
    };

    return (
        <div className="p-4 border rounded-lg shadow-sm">
            <h3 className="text-lg font-medium mb-4">Upload Invoice</h3>
            <input
                type="file"
                accept=".xlsx,.xls"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="mb-4 block w-full text-sm text-gray-500 
                          file:mr-4 file:py-2 file:px-4 
                          file:rounded-md file:border-0 
                          file:text-sm file:font-medium 
                          file:bg-blue-50 file:text-blue-700 
                          hover:file:bg-blue-100 hover:file:text-blue-800
                          file:cursor-pointer file:transition-all file:duration-200
                          cursor-pointer"
            />
            <Button
                onClick={handleUpload}
                disabled={!file || loading}
                size="default"
                className="transition-all duration-200 hover:scale-105 hover:shadow-md"
            >
                {loading ? 'Processing...' : 'Upload & Process'}
            </Button>
        </div>
    );
}