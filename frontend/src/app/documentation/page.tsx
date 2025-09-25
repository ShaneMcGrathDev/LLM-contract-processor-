'use client';

import { AppSidebar } from "@/components/app-sidebar";
import { SidebarInset, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { FileText } from "lucide-react";

export default function DocumentationPage() {
    // Your markdown content goes here
    const markdownContent = `
# Invoice Processor - Project Documentation Page

## Project Overview

This is a web application designed so users can submit invoice files, extract and structure relevant data, view and edit the data, and submit the invoice details to a database.

## Technologies Used

### Frontend
- **Next.js** - React framework for the user interface
- **Shadcn UI Library** - Modern component library for consistent styling

### Backend
- *Flask* - Python web framework for API endpoints
- **Claude LLM API** - AI-powered invoice data extraction
- **Supabase** - PostgreSQL database hosting and management

## Getting Started

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

### AI-Powered Extraction
Our system uses **Claude AI** to intelligently extract data from various invoice formats:
- Recognizes different field names (e.g., "Total Due" vs "Amount Due")
- Handles scattered data layouts
- Processes both table and form-based invoices

### Smart Field Mapping
The system automatically maps field variations:
- \`TotalDue\` → Total Amount
- \`Tax Rate\` → Tax Amount (when it contains dollar amounts)
- \`Invoice Subtotal\` → Subtotal

### Performance Optimized
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

## Future Enhancements & Scaling Strategy

### Anticipated Operational Challenges

**Higher Volumes**
Our company has a history of consistent growth with expanding customer, employee, and supplier populations. Software usage tends to follow this growth curve, especially in areas where headcount scales with business growth.

- Every invoice processed has 2,000-6,000 tokens per Claude transaction overhead
- Higher volumes may strain rate limits in future state
- Current architecture suitable for 100-1,000 users based on research

**Diversified User Base & Use Cases**
One key design challenge is broadly solving for common challenges across diverse business units with localized nuance.

- Different business areas use varied terminology
- Same words often describe different concepts across divisions
- Future applications should capture requirements dynamically rather than building one solution per requirement

**Diversified Process Needs**
New acquisitions and product launches necessitate new workflows and application requirements.

- LLM pattern recognition fits well as part of overall strategy
- Pairing with thoughtful in-house algorithms expands flexibility for diverse needs

### Enhancement Ideas

**Dynamic Prompting Generation**
Develop intermediary functions that analyze datasets and generate dynamic prompting structures.

Benefits:
- Handle wider array of edge cases
- Expand explicit requirements without major code overhaul
- More flexible solutioning approach

**Two-Tiered Model Approach**
Current expensive Claude transactions could handle 100-1,000 users, but individual activity levels could strain architecture.

- Funnel common cases to simpler open source LLM models
- Reserve Claude for complex/emergent cases
- Cost optimization while maintaining capability

**Batch Processing**
For rising submission volumes, stage and process files/data in batches at scheduled times.

**User Analytics Implementation**
Create analytics tracking:
- Usage volume patterns
- Geographic distribution
- Business unit utilization

## Technical Learnings & Challenges

### API & Model Selection
- Hit free-tier rate limit on Gemini model API, switched to Claude
- Beneficial exercise comparing different LLM setups and API configurations

### Infrastructure & Connectivity
- Switched from IPv6 to IPv4 for connectivity issues
- First time setting up Supabase database
- Connecting LLM API to full stack application

### Development Techniques
- Using PowerShell hash tables to load test data via JSON payloads
- OS library seek method for file pointer and byte position measurement
- Chrome Developer Tools network tab for request analysis
- Python request object for concurrent HTTP requests in CRUD operations

### Backend Development
- Direct hands-on work with database models in Flask
- Building backend from ground up with Blueprints, routes, models, services/utilities
- Creative problem-solving with Claude model prompting within routes

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
- \`GET /api/invoices\` - List all saved invoices
- \`GET /api/invoices/<id>\` - Get specific invoice
- \`DELETE /api/invoices/<id>\` - Delete invoice

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

## Project Reflection

This case study provided an opportunity to combine new skills with existing ones while working with emerging technologies and exploring AI capabilities in a business context.

### Key Takeaways
- Valuable exposure to different LLM model configurations
- Deepened backend development skills across Blueprint, routes, models, and services
- Creative problem-solving with LLM prompting and edge case handling
- Practical experience with full-stack AI integration

### Areas for Improvement
- Consider providing sample invoices upfront for testing
- More specific guidance on example data usage
- Clearer instruction on what elements are essential vs. optional

---

## Need Help?

If you have questions or need assistance:
- Check this documentation first
- Review the troubleshooting section
- Contact our support team
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