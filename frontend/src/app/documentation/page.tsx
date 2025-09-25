'use client';

import { AppSidebar } from "@/components/app-sidebar";
import { SidebarInset, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { FileText } from "lucide-react";

export default function DocumentationPage() {
    // Your markdown content goes here
    const markdownContent = `

# Case Study Project Overview

Welcome! This documentation covers reflections and insights into the development process for this full stack web application which leverages AI to process diverse Excel based invoice files.

Users can submit invoice files to extract and structure relevant data, view and edit the data, and submit the invoice details to a database.

## Technologies Used

**Frontend**
- Next.js (Frontend architecture)
- Shadcn UI library (To enhance UI/UX)
**Backend**
- Flask (Backend)
- Claude LLM API (Core processing capability)
- Supabase (Postgres database)

## Future Enhancements/Scaling Strategy

Three conditions could create operational challenges in the future state for the invoice solution as conditions change in the operating environment:

### Condition #1: Rising user and/or file volumes 

- Customer, employee, and supplier populations grow over time in successful companies
- Software application usage tends to follow this growth curve, especially in areas where headcount scales with business growth
- Every invoice processed has an overhead tied to it (2,000-6,000 tokens per Claude transaction estimated)
- Higher volumes may strain rate limits in future state

### Condition #2: Diversified user base, plurality of use cases, flexible capability 

- The invoice processor will have evolving requirements over time based on condition one, with adjacent use cases emerging
- One key design challenge is to broadly solve for common challenges in diverse business units that have localized nuance
- Language and terminology applicable to different business areas is very diverse - often two businesses use the same word to describe different things
- One approach is to anticipate diverse and evolving use case flow with dynamic solutioning captured in algorithms rather than explicitly solving for individual use cases
- The pattern recognition of LLM seems like a good fit as part of the overall strategy, paired with thoughtful algorithms that expand flexibility

### Condition #3: Evolving software ecosystem of the organization 

- To what extent can custom software solutions interface with vendor solutions in a coherent manner
- Incompatibility drives inefficiencies and manual workarounds
- Building connectivity between different systems over time and enabling coherent functionality will be important

## Four Ideas for Further Development

### 1. Dynamic prompting generation with intermediary functions

Develop an intermediary function between initial file packet response to backend and Claude processing that analyzes the dataset and generates a dynamic structure for the prompting.

**Benefits:** Could deal with a wider array of edge cases and expand the number of explicit requirements the algorithms can potentially handle, potentially avoiding major code base overhauls as needs evolve.

### 2. Dual/Multiple LLM model approach

Based on research, the current application using expensive Claude transactions could potentially handle volume in the range of 100-1000 users. Individual activity levels could compound and strain this architecture eventually.

It may be better to funnel some volume to simpler open source LLM models with less capability for common cases, leaving emergent cases to the Claude model.

### 3. Batch processing of invoice files

If submission volumes rise as per condition one, it may make sense to stage and process files/data in batches at a later time.

### 4. Create user usage analytics

Track volume, geography, and business unit usage patterns.

## Things I Learned and Challenges

### 1. LLM model switch and subsequent refactor

Hit a free-tier rate limit on the Gemini model API, so had to switch to Claude which required backend refactoring.

### 2. Supabase connection parameter challenge

I ran into an IPv4/IPv6 networking issue when setting up my Flask backend with Supabase database connection. As a solution I switched from the direct database connection to Supabase's pooled connection option, which likely defaulted to using IPv4 instead of IPv6, and it worked perfectly.

### 3. Command line functionality

In experimenting with how to test database additions, I learned how to pass a JSON payload using PowerShell hash tables through the terminal to load test data into the database and test the connection.

### 4. Python OS library deeper functionality

The seek method from the OS library uses a file pointer to look at the byte position of a file, useful for measuring file size in data related operations.

### 5. Developer tools deeper functionality

Using the network tab in Chrome Developer tools to look at request headers, body, etc., very useful for backend work.

### 6. Learning about concurrent request capability

The request object in Python Flask allows for concurrent HTTP requests in CRUD operations. Interesting implication for more sophisticated applications.

### 7. Hands on time with database models

More direct hands-on work with database models within Flask.

### 8. Setting up a Supabase database for the first time

### 9. Connecting an LLM API to a full stack application for the first time

## Feedback/Reflection on This Case Study

This case study was a great opportunity to combine new skills with existing ones, work with some new tech, and go deeper on AI and their capabilities in a business context.

- It was a beneficial exercise to go "shopping" for an LLM model and get exposure to some different setups, API configs, etc.

- I also enjoyed building the backend from the ground up and spending more time in the various sections to deepen my skills (e.g. Blueprint, routes, models, services/utilities).

- I learned a lot working in the route to get the LLM processing working and enjoyed the chance to test out different invoices and stumble upon some edge cases in the data fields.

- I had some good creative thinking moments working with the prompting of the Claude model within the route, and had the idea to generate dynamic prompts in future state.

### Ideas on how to refine the case study format

- Consider creating and providing a handful of invoices up front to test and work with the data
- Share some ways the team is currently leveraging data as a supplemental read through, what they've learned, opportunities/challenges, etc.
- Some more specific instruction for what to do with the example data and what is not needed would be helpful. Found myself overthinking this stage of the project
`;

    // GitHub-style markdown parser with tight spacing
    const parseMarkdown = (markdown) => {
        return markdown
            // First, handle line breaks and paragraphs properly
            .split('\n\n')
            .map(block => {
                // Headers
                if (block.startsWith('### ')) {
                    return `<h3 class="text-lg font-semibold mt-6 mb-2 text-gray-900">${block.slice(4)}</h3>`;
                }
                if (block.startsWith('## ')) {
                    return `<h2 class="text-xl font-bold mt-8 mb-3 text-blue-900">${block.slice(3)}</h2>`;
                }
                if (block.startsWith('# ')) {
                    return `<h1 class="text-2xl font-bold mt-4 mb-4 text-gray-900 border-b border-gray-200 pb-2">${block.slice(2)}</h1>`;
                }

                // Lists
                if (block.includes('\n- ') || block.startsWith('- ')) {
                    const listItems = block
                        .split('\n')
                        .filter(line => line.startsWith('- '))
                        .map(line => `<li class="text-gray-700">${line.slice(2)}</li>`)
                        .join('');
                    return `<ul class="list-disc pl-6 mb-4 space-y-1">${listItems}</ul>`;
                }

                // Regular paragraphs
                return `<p class="mb-4 text-gray-700 leading-relaxed">${block}</p>`;
            })
            .join('')

            // Bold and italic
            .replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold">$1</strong>')
            .replace(/\*(.*?)\*/g, '<em class="italic">$1</em>')

            // Inline code
            .replace(/`([^`]*)`/g, '<code class="bg-gray-100 text-gray-800 px-1 py-0.5 rounded text-sm font-mono">$1</code>')

            // Clean up empty paragraphs
            .replace(/<p class="mb-4 text-gray-700 leading-relaxed"><\/p>/g, '');
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
                        <div className="p-8 border rounded-lg shadow-sm bg-white">
                            <div
                                className="max-w-none"
                                dangerouslySetInnerHTML={{ __html: parseMarkdown(markdownContent) }}
                            />
                        </div>
                    </div>
                </div>
            </SidebarInset>
        </SidebarProvider>
    );
}