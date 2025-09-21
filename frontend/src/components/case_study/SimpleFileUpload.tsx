'use client';

import { useState } from 'react';

export default function SimpleFileUpload() {
    const [file, setFile] = useState<File | null>(null);
    const [response, setResponse] = useState<any>(null);

    const handleUpload = async () => {
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        const res = await fetch('http://localhost:5000/api/upload-png', {
            method: 'POST',
            body: formData,
        });

        setResponse(await res.json());
    };

    return (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Upload PNG</h3>

            <input
                type="file"
                accept=".png"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="mb-4 block w-full text-sm text-gray-500"
            />

            <button
                onClick={handleUpload}
                disabled={!file}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400"
            >
                Upload
            </button>

            {response && (
                <div className="mt-4 p-3 bg-gray-50 rounded-md text-sm">
                    {JSON.stringify(response, null, 2)}
                </div>
            )}
        </div>
    );
}