'use client';

import { useState } from 'react';
import { AppSidebar } from "@/components/app-sidebar";
import { SidebarInset, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import InvoiceProcessor from '@/components/invoice-processor/InvoiceProcessor';
import InvoiceEditor from '@/components/invoice-editor/InvoiceEditor';

export default function Home() {
    const [invoiceData, setInvoiceData] = useState(null);

    return (
        <SidebarProvider>
            <AppSidebar />
            <SidebarInset>
                <header className="flex h-16 items-center gap-2 px-4">
                    <SidebarTrigger />
                    <h1 className="text-lg font-semibold">Invoice Processing</h1>
                </header>

                <div className="flex-1 p-4 space-y-4">
                    <div className="w-full md:w-1/2 ml-0 md:ml-8">
                        <InvoiceProcessor onDataReceived={setInvoiceData} />
                        {invoiceData && <div className="mt-4"><InvoiceEditor data={invoiceData} /></div>}
                    </div>
                </div>
            </SidebarInset>
        </SidebarProvider>
    );
}