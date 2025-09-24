'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';

export default function ClaudeTest({ onDataReceived }) {
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
            }
        } catch (error) {
            console.error('Upload failed:', error);
        }
        setLoading(false);
    };

    return (
        <div className="p-4 border rounded-lg shadow-md">
            <h3 className="text-lg font-medium mb-4">Upload Invoice</h3>
            <input
                type="file"
                accept=".xlsx,.xls"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="mb-4 block w-full"
            />
            <Button
                onClick={handleUpload}
                disabled={!file || loading}
                size="default"
            >
                {loading ? 'Processing...' : 'Upload & Process'}
            </Button>
        </div>
    );
}