'use client';

import { useState } from 'react';

export default function Page() {
    const [inputNumber, setInputNumber] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [response, setResponse] = useState(null);
    const [file, setFile] = useState<File | null>(null);
    const [fileResponse, setFileResponse] = useState<any>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            const res = await fetch('http://localhost:5000/api/submit-number', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ number: parseInt(inputNumber) }),
            });

            const data = await res.json();
            setResponse(data);
        } catch (error) {
            setResponse({ error: 'Failed to submit number' });
        } finally {
            setIsLoading(false);
        }
    };

    const handleFileUpload = async () => {
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const res = await fetch('http://localhost:5000/api/upload-png', {
                method: 'POST',
                body: formData,
            });

            const data = await res.json();
            setFileResponse(data);
        } catch (error) {
            setFileResponse({ error: 'Failed to upload file' });
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">Invoice Extraction Tool</h1>
                    <p className="text-gray-600 mt-2"></p>
                </div>

                {/* Cards Container */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                        <h3 className="text-lg font-medium text-gray-900 mb-4">Upload PNG</h3>

                        <input
                            type="file"
                            accept=".png"
                            onChange={(e) => setFile(e.target.files?.[0] || null)}
                            className="mb-4 block w-full text-sm text-gray-500"
                        />

                        <button
                            onClick={handleFileUpload}
                            disabled={!file}
                            className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
                        >
                            Upload
                        </button>

                        {fileResponse && (
                            <div className="mt-4 p-3 bg-gray-50 rounded-md">
                                <p className="text-sm text-gray-600">Response:</p>
                                <p className="text-sm font-mono text-gray-900">{JSON.stringify(fileResponse, null, 2)}</p>
                            </div>
                        )}
                    </div>

                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                        <h3 className="text-lg font-medium text-gray-900 mb-2">Another Card</h3>
                        <p className="text-gray-600">More card content here</p>
                    </div>

                    {/* <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                        <h3 className="text-lg font-medium text-gray-900 mb-2">Third Card</h3>
                        <p className="text-gray-600">Even more content</p>
                    </div> */}
                </div>
            </div>
        </div >
    );
}