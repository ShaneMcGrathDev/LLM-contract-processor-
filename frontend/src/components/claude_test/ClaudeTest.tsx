'use client';

import { useState } from 'react';

export default function ClaudeTest() {
    const [file, setFile] = useState<File | null>(null);
    const [response, setResponse] = useState<any>(null);
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
            setResponse(await res.json());
        } catch (error) {
            setResponse({ error: 'Upload failed' });
        }
        setLoading(false);
    };

    return (
        <div className="p-6 border rounded-lg">
            <h3 className="text-lg font-medium mb-4">Invoice Upload</h3>
            <input type="file" accept=".xlsx,.xls" onChange={(e) => setFile(e.target.files?.[0] || null)} className="mb-4" />
            <button onClick={handleUpload} disabled={!file || loading} className="bg-blue-600 text-white px-4 py-2 rounded disabled:bg-gray-400">
                {loading ? 'Processing...' : 'Upload'}
            </button>
            {response && <pre className="mt-4 p-3 bg-gray-100 rounded text-sm overflow-auto">{JSON.stringify(response, null, 2)}</pre>}
        </div>
    );
}