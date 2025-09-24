'use client';

import { AppSidebar } from "@/components/app-sidebar";
import { SidebarInset, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { FileText } from "lucide-react";

export default function DocumentationPage() {
    // Your markdown content goes here
    const markdownContent = `
# Case Study 2025: Invoice Processor Documentation

## Application Developed by Shane McGrath September 2025

Welcome to the **Invoice Processor** documentation! This guide will help you understand how to use our AI-powered invoice processing system.

## Overview 

### Step 1: Upload Your Invoice
1. Click the **"Choose file"** button
2. Select an Excel invoice file (.xlsx or .xls)
3. Click **"Upload & Process"**

### Step 2: Review Extracted Data
After processing, you'll see the extracted invoice data in an editable form:
- **Vendor Name**: The company that sent the invoice
- **Subtotal**: Amount before taxes and fees
- **Tax Amount**: Total tax charged
- **Freight Amount**: Shipping and handling costs
- **Total Amount**: Final amount due

### Step 3: Edit and Save
- Make any necessary corrections to the extracted data
- Click **"Save to Database"** to store the invoice
- Use **"More Details"** to see a comprehensive view

## Features

### 🤖 AI-Powered Extraction
Our system uses **Claude AI** to intelligently extract data from various invoice formats:
- Recognizes different field names (e.g., "Total Due" vs "Amount Due")
- Handles scattered data layouts
- Processes both table and form-based invoices

### 📊 Smart Field Mapping
The system automatically maps field variations:
- \`TotalDue\` → Total Amount
- \`Tax Rate\` → Tax Amount (when it contains dollar amounts)
- \`Invoice Subtotal\` → Subtotal

### ⚡ Performance Optimized
- **Fast processing**: Typically 3-10 seconds
- **Data efficiency**: Only relevant data sent to AI
- **Smart text cleaning**: Removes unnecessary formatting

## Supported File Formats

| Format | Extension | Support Level |
|--------|-----------|---------------|
| Excel 2007+ | .xlsx | ✅ Full Support |
| Excel 97-2003 | .xls | ✅ Full Support |
| CSV | .csv | 🚧 Coming Soon |
| PDF | .pdf | 🚧 Coming Soon |

## Common Invoice Fields

The system can extract these common fields:

### Basic Information
- Vendor/Supplier Name
- Customer/Bill To Name
- Invoice Number
- Invoice Date
- Due Date

### Financial Data
- Line Items (description, quantity, price)
- Subtotal
- Tax Amount
- Freight/Shipping
- Discounts
- **Total Amount**

## Tips for Better Results

### 📋 File Preparation
- Ensure invoice data is clearly visible
- Avoid heavily formatted or image-based invoices
- Clean, structured data works best

### 🔍 Review Process
- Always review extracted data for accuracy
- Pay special attention to financial amounts
- Use the "More Details" view for comprehensive checking

### 💾 Data Management
- Save processed invoices to build your database
- Use consistent vendor naming for better organization
- Regular backups recommended

## Troubleshooting

### Upload Issues
**Problem**: File won't upload
- ✅ Check file format (.xlsx or .xls only)
- ✅ Ensure file size is under 10MB
- ✅ Verify file isn't corrupted

### Processing Errors
**Problem**: "Processing failed" message
- ✅ Check your internet connection
- ✅ Try a different invoice file
- ✅ Contact support if issue persists

### Accuracy Issues
**Problem**: Incorrect data extraction
- ✅ Use the edit form to make corrections
- ✅ Check if invoice format is unusual
- ✅ Consider manual entry for complex layouts

## API Information

### Backend Routes
- \`POST /api/claude_test\` - Process invoice with AI
- \`POST /api/review-invoice\` - Save edited invoice data

### Response Format
\`\`\`json
{
  "success": true,
  "data": {
    "vendor_name": "Company Name",
    "subtotal": 1000.00,
    "tax_amount": 80.00,
    "total_amount": 1080.00,
    "confidence": "high"
  }
}
\`\`\`

## Security & Privacy

### Data Handling
- All invoice data is processed securely
- No data stored on external AI servers permanently
- Local database storage for your records only

### Best Practices
- Don't upload invoices with sensitive personal information
- Regularly review and clean your database
- Keep backups of important invoice data

---

## Need Help?

If you have questions or need assistance:
- Check this documentation first
- Review the troubleshooting section
- Contact our support team

**Happy processing!** 🚀
  `;

    // Simple function to convert markdown to HTML (basic implementation)
    const parseMarkdown = (markdown) => {
        return markdown
            // Headers
            .replace(/^### (.*$)/gim, '<h3 class="text-lg font-semibold mt-6 mb-3">$1</h3>')
            .replace(/^## (.*$)/gim, '<h2 class="text-xl font-bold mt-8 mb-4 text-blue-900">$1</h2>')
            .replace(/^# (.*$)/gim, '<h1 class="text-2xl font-bold mt-6 mb-6 text-gray-900 border-b pb-2">$1</h1>')

            // Bold and italic
            .replace(/\*\*(.*)\*\*/gim, '<strong class="font-semibold">$1</strong>')
            .replace(/\*(.*)\*/gim, '<em class="italic">$1</em>')

            // Code blocks and inline code
            .replace(/```json\n([\s\S]*?)\n```/gim, '<pre class="bg-gray-100 rounded-lg p-4 mt-4 mb-4 overflow-x-auto"><code class="text-sm">$1</code></pre>')
            .replace(/```([\s\S]*?)```/gim, '<pre class="bg-gray-100 rounded-lg p-4 mt-4 mb-4 overflow-x-auto"><code class="text-sm">$1</code></pre>')
            .replace(/`([^`]*)`/gim, '<code class="bg-gray-100 px-2 py-1 rounded text-sm font-mono">$1</code>')

            // Tables
            .replace(/^\|(.+)\|$/gim, '<tr>$1</tr>')
            .replace(/\|([^|]*)\|/gim, '<td class="border px-4 py-2">$1</td>')

            // Lists
            .replace(/^- (.*$)/gim, '<li class="ml-4 mb-1">• $1</li>')
            .replace(/^✅ (.*$)/gim, '<li class="ml-4 mb-1 text-green-600">✅ $1</li>')
            .replace(/^🚧 (.*$)/gim, '<li class="ml-4 mb-1 text-yellow-600">🚧 $1</li>')
            .replace(/^❌ (.*$)/gim, '<li class="ml-4 mb-1 text-red-600">❌ $1</li>')

            // Paragraphs
            .replace(/\n\n/gim, '</p><p class="mb-4">')
            .replace(/\n/gim, '<br/>')

            // Wrap in paragraphs
            .replace(/^(?!<[h|l|p|d|u])(.+)$/gim, '<p class="mb-4">$1</p>')

            // Clean up
            .replace(/<p class="mb-4"><\/p>/gim, '');
    };

    return (
        <SidebarProvider>
            <AppSidebar />
            <SidebarInset>
                <header className="flex h-16 items-center gap-2 px-4 border-b">
                    <SidebarTrigger />
                    <div className="flex items-center gap-2">
                        <FileText className="h-5 w-5 text-blue-600" />
                        <h1 className="text-lg font-semibold">Documentation</h1>
                    </div>
                </header>

                <div className="flex-1 p-4">
                    <div className="w-full md:w-2/3 ml-0 md:ml-8">
                        <div className="p-6 border rounded-lg shadow-sm bg-white">
                            <div
                                className="prose prose-sm max-w-none"
                                dangerouslySetInnerHTML={{ __html: parseMarkdown(markdownContent) }}
                            />
                        </div>
                    </div>
                </div>
            </SidebarInset>
        </SidebarProvider>
    );
}