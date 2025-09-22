'use client';

import { useState } from 'react';
import ExcelUpload from "@/components/case_study/ExcelUpload";

export default function Page() {

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">Invoice Extraction Tool</h1>
                    <p className="text-gray-600 mt-2"></p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                        <h3 className="text-lg font-medium text-gray-900 mb-2">Another Card</h3>
                        <p className="text-gray-600">More card content here</p>
                        <ExcelUpload />
                    </div>
                </div>
            </div>
        </div >
    );
}