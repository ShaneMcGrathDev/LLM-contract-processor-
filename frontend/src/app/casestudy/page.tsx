'use client';

import { useState } from 'react';

export default function Page() {
    const [inputNumber, setInputNumber] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [response, setResponse] = useState(null);

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

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
                    <p className="text-gray-600 mt-2">Welcome to your dashboard</p>
                </div>

                {/* Cards Container */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {/* Number Input Card */}
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                        <h3 className="text-lg font-medium text-gray-900 mb-4">Submit Number</h3>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div>
                                <label htmlFor="number" className="block text-sm font-medium text-gray-700 mb-2">
                                    Enter a number:
                                </label>
                                <input
                                    type="number"
                                    id="number"
                                    value={inputNumber}
                                    onChange={(e) => setInputNumber(e.target.value)}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                    placeholder="Enter number..."
                                    required
                                />
                            </div>
                            <button
                                type="submit"
                                disabled={isLoading}
                                className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed"
                            >
                                {isLoading ? 'Submitting...' : 'Submit'}
                            </button>
                        </form>

                        {/* Response Display */}
                        {response && (
                            <div className="mt-4 p-3 bg-gray-50 rounded-md">
                                <p className="text-sm text-gray-600">Response:</p>
                                <p className="text-sm font-mono text-gray-900">{JSON.stringify(response, null, 2)}</p>
                            </div>
                        )}
                    </div>

                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                        <h3 className="text-lg font-medium text-gray-900 mb-2">Another Card</h3>
                        <p className="text-gray-600">More card content here</p>
                    </div>

                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                        <h3 className="text-lg font-medium text-gray-900 mb-2">Third Card</h3>
                        <p className="text-gray-600">Even more content</p>
                    </div>
                </div>
            </div>
        </div>
    );
}