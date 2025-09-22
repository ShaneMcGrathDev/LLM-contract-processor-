'use client';

import { useState } from 'react';

interface ExcelUploadResponse {
    message?: string;
    filename?: string;
    error?: string;
    extracted_data?: any;
}

export default function ExcelUpload() {
    const [file, setFile] = useState<File | null>(null);
    const [response, setResponse] = useState<ExcelUploadResponse | null>(null);
    const [isUploading, setIsUploading] = useState<boolean>(false);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = event.target.files?.[0];

        if (selectedFile) {
            // Validate Excel file types
            const validTypes = [
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', // .xlsx
                'application/vnd.ms-excel', // .xls
                'text/csv' // .csv
            ];

            if (validTypes.includes(selectedFile.type)) {
                setFile(selectedFile);
                setResponse(null);
            } else {
                alert('Please select an Excel file (.xlsx, .xls, or .csv)');
                event.target.value = '';
            }
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setIsUploading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            const res = await fetch('http://localhost:5000/api/upload-excel', {
                method: 'POST',
                body: formData,
            });

            const data: ExcelUploadResponse = await res.json();
            setResponse(data);

            if (res.ok) {
                setFile(null);
                // Clear the file input
                const fileInput = document.getElementById('excel-file') as HTMLInputElement;
                if (fileInput) fileInput.value = '';
            }
        } catch (error) {
            setResponse({ error: 'Failed to upload Excel file' });
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Upload Excel File</h3>

            <input
                id="excel-file"
                type="file"
                accept=".xlsx,.xls,.csv,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel,text/csv"
                onChange={handleFileChange}
                className="mb-4 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            />

            {file && (
                <div className="mb-4 p-3 bg-gray-50 rounded-md">
                    <p className="text-sm text-gray-600">Selected file:</p>
                    <p className="text-sm font-medium text-gray-900">{file.name}</p>
                    <p className="text-xs text-gray-500">
                        Size: {(file.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                </div>
            )}

            <button
                onClick={handleUpload}
                disabled={!file || isUploading}
                className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
                {isUploading ? 'Uploading...' : 'Upload Excel File'}
            </button>

            {response && (
                <div className="mt-4 p-3 bg-gray-50 rounded-md">
                    <p className="text-sm text-gray-600">Response:</p>
                    <pre className="text-sm font-mono text-gray-900 whitespace-pre-wrap">
                        {JSON.stringify(response, null, 2)}
                    </pre>
                </div>
            )}
        </div>
    );
}