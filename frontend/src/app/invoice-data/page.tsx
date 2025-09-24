'use client';

import { useEffect, useState } from 'react';
import { AppSidebar } from "@/components/app-sidebar";
import { SidebarInset, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { ArrowLeft, FileText, DollarSign, Calendar, Building } from "lucide-react";
import { useRouter } from 'next/navigation';

export default function InvoiceDataPage() {
    const router = useRouter();
    const [invoiceData, setInvoiceData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        console.log('🔍 Debug: Loading invoice data page...');

        // Get data from localStorage
        const storedData = localStorage.getItem('currentInvoiceData');
        console.log('📦 Raw stored data:', storedData);

        if (storedData) {
            try {
                const parsedData = JSON.parse(storedData);
                console.log('✅ Successfully parsed data:', parsedData);
                console.log('📊 Data keys:', Object.keys(parsedData));
                setInvoiceData(parsedData);
            } catch (error) {
                console.error('❌ Error parsing invoice data:', error);
            }
        } else {
            console.log('❌ No stored data found in localStorage');

            // Also check if there are any localStorage keys at all
            console.log('🗂️ All localStorage keys:', Object.keys(localStorage));
        }
        setLoading(false);
    }, []);

    if (loading) {
        return (
            <SidebarProvider>
                <AppSidebar />
                <SidebarInset>
                    <div className="flex items-center justify-center h-screen">
                        <div className="text-center">
                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
                            <p>Loading invoice data...</p>
                        </div>
                    </div>
                </SidebarInset>
            </SidebarProvider>
        );
    }

    if (!invoiceData) {
        return (
            <SidebarProvider>
                <AppSidebar />
                <SidebarInset>
                    <div className="flex items-center justify-center h-screen">
                        <div className="text-center">
                            <FileText className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                            <h2 className="text-xl font-semibold mb-2">No Invoice Data Found</h2>
                            <p className="text-gray-600 mb-4">Please process an invoice first.</p>
                            <Button onClick={() => router.push('/')}>
                                <ArrowLeft className="h-4 w-4 mr-2" />
                                Back to Upload
                            </Button>
                        </div>
                    </div>
                </SidebarInset>
            </SidebarProvider>
        );
    }

    const getConfidenceColor = (confidence) => {
        switch (confidence?.toLowerCase()) {
            case 'high': return 'bg-green-500';
            case 'medium': return 'bg-yellow-500';
            case 'low': return 'bg-red-500';
            default: return 'bg-gray-500';
        }
    };

    return (
        <SidebarProvider>
            <AppSidebar />
            <SidebarInset>
                <header className="flex h-16 items-center gap-2 px-4 border-b">
                    <SidebarTrigger />
                    <div className="flex items-center gap-2">
                        <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => router.back()}
                        >
                            <ArrowLeft className="h-4 w-4 mr-2" />
                            Back
                        </Button>
                        <h1 className="text-lg font-semibold">Invoice Data Details</h1>
                    </div>
                    {invoiceData?.confidence && (
                        <Badge className={`${getConfidenceColor(invoiceData.confidence)} text-white ml-auto`}>
                            {invoiceData.confidence} Confidence
                        </Badge>
                    )}
                </header>

                <div className="flex-1 p-6 space-y-6">
                    {/* Summary Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Vendor</CardTitle>
                                <Building className="h-4 w-4 text-muted-foreground" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-lg font-bold">{invoiceData.vendor_name || 'N/A'}</div>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Invoice Date</CardTitle>
                                <Calendar className="h-4 w-4 text-muted-foreground" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-lg font-bold">{invoiceData.invoice_date || 'N/A'}</div>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Subtotal</CardTitle>
                                <DollarSign className="h-4 w-4 text-muted-foreground" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-lg font-bold">${invoiceData.subtotal?.toFixed(2) || '0.00'}</div>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Total Amount</CardTitle>
                                <DollarSign className="h-4 w-4 text-muted-foreground" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold text-green-600">
                                    ${invoiceData.total_amount?.toFixed(2) || '0.00'}
                                </div>
                            </CardContent>
                        </Card>
                    </div>

                    {/* Detailed Information Table */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Invoice Details</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <Table>
                                <TableHeader>
                                    <TableRow>
                                        <TableHead className="w-[200px]">Field</TableHead>
                                        <TableHead>Value</TableHead>
                                        <TableHead className="w-[150px]">Source Field</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    <TableRow>
                                        <TableCell className="font-medium">Vendor Name</TableCell>
                                        <TableCell>{invoiceData.vendor_name || 'N/A'}</TableCell>
                                        <TableCell className="text-sm text-muted-foreground">
                                            {invoiceData.field_mappings_used?.vendor_source || 'Auto-detected'}
                                        </TableCell>
                                    </TableRow>

                                    <TableRow>
                                        <TableCell className="font-medium">Customer Name</TableCell>
                                        <TableCell>{invoiceData.customer_name || 'N/A'}</TableCell>
                                        <TableCell className="text-sm text-muted-foreground">
                                            {invoiceData.field_mappings_used?.customer_source || 'Auto-detected'}
                                        </TableCell>
                                    </TableRow>

                                    <TableRow>
                                        <TableCell className="font-medium">Invoice Number</TableCell>
                                        <TableCell>{invoiceData.invoice_number || 'N/A'}</TableCell>
                                        <TableCell className="text-sm text-muted-foreground">Auto-detected</TableCell>
                                    </TableRow>

                                    <TableRow>
                                        <TableCell className="font-medium">Invoice Date</TableCell>
                                        <TableCell>{invoiceData.invoice_date || 'N/A'}</TableCell>
                                        <TableCell className="text-sm text-muted-foreground">Auto-detected</TableCell>
                                    </TableRow>

                                    <TableRow>
                                        <TableCell className="font-medium">Due Date</TableCell>
                                        <TableCell>{invoiceData.due_date || 'N/A'}</TableCell>
                                        <TableCell className="text-sm text-muted-foreground">Auto-detected</TableCell>
                                    </TableRow>

                                    <TableRow>
                                        <TableCell className="font-medium">Subtotal</TableCell>
                                        <TableCell className="font-mono">${invoiceData.subtotal?.toFixed(2) || '0.00'}</TableCell>
                                        <TableCell className="text-sm text-muted-foreground">Auto-detected</TableCell>
                                    </TableRow>

                                    <TableRow>
                                        <TableCell className="font-medium">Tax Amount</TableCell>
                                        <TableCell className="font-mono">${invoiceData.tax_amount?.toFixed(2) || '0.00'}</TableCell>
                                        <TableCell className="text-sm text-muted-foreground">
                                            {invoiceData.field_mappings_used?.tax_source || 'Auto-detected'}
                                        </TableCell>
                                    </TableRow>

                                    {invoiceData.freight_amount && (
                                        <TableRow>
                                            <TableCell className="font-medium">Freight Amount</TableCell>
                                            <TableCell className="font-mono">${invoiceData.freight_amount?.toFixed(2) || '0.00'}</TableCell>
                                            <TableCell className="text-sm text-muted-foreground">
                                                {invoiceData.field_mappings_used?.freight_source || 'Auto-detected'}
                                            </TableCell>
                                        </TableRow>
                                    )}

                                    <TableRow className="bg-green-50">
                                        <TableCell className="font-bold">Total Amount</TableCell>
                                        <TableCell className="font-mono font-bold text-green-700">
                                            ${invoiceData.total_amount?.toFixed(2) || '0.00'}
                                        </TableCell>
                                        <TableCell className="text-sm text-muted-foreground">
                                            {invoiceData.field_mappings_used?.total_source || 'Auto-detected'}
                                        </TableCell>
                                    </TableRow>
                                </TableBody>
                                <TableCaption>
                                    Extracted invoice data with field mapping sources
                                </TableCaption>
                            </Table>
                        </CardContent>
                    </Card>

                    {/* Line Items Table */}
                    {invoiceData.line_items && invoiceData.line_items.length > 0 && (
                        <Card>
                            <CardHeader>
                                <CardTitle>Line Items ({invoiceData.line_items.length})</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <Table>
                                    <TableHeader>
                                        <TableRow>
                                            <TableHead>Description</TableHead>
                                            <TableHead className="w-[100px]">Qty</TableHead>
                                            <TableHead className="w-[120px]">Unit Price</TableHead>
                                            <TableHead className="w-[120px] text-right">Total</TableHead>
                                        </TableRow>
                                    </TableHeader>
                                    <TableBody>
                                        {invoiceData.line_items.map((item, index) => (
                                            <TableRow key={index}>
                                                <TableCell>{item.description || 'N/A'}</TableCell>
                                                <TableCell>{item.quantity || 0}</TableCell>
                                                <TableCell className="font-mono">${item.unit_price?.toFixed(2) || '0.00'}</TableCell>
                                                <TableCell className="font-mono text-right font-medium">
                                                    ${item.total?.toFixed(2) || '0.00'}
                                                </TableCell>
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                    <TableCaption>
                                        Individual line items from the invoice
                                    </TableCaption>
                                </Table>
                            </CardContent>
                        </Card>
                    )}
                </div>
            </SidebarInset>
        </SidebarProvider>
    );
}