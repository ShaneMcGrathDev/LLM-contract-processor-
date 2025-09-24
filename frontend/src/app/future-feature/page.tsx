'use client';

import { AppSidebar } from "@/components/app-sidebar";
import { SidebarInset, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
    HoverCard,
    HoverCardContent,
    HoverCardTrigger,
} from "@/components/ui/hover-card";
import { Sparkles, Clock, Zap, Brain, FileText, BarChart3 } from "lucide-react";

export default function FutureFeaturePage() {
    const upcomingFeatures = [
        {
            title: "AI Batch Processing",
            description: "Process multiple invoices simultaneously",
            icon: Brain,
            status: "Coming Soon"
        },
        {
            title: "Smart Analytics Dashboard",
            description: "Insights and trends from your invoice data",
            icon: BarChart3,
            status: "In Development"
        },
        {
            title: "Auto-categorization",
            description: "Automatically sort invoices by vendor and type",
            icon: FileText,
            status: "Planning Phase"
        },
        {
            title: "Real-time Processing",
            description: "Lightning-fast invoice processing with WebSockets",
            icon: Zap,
            status: "Research Phase"
        }
    ];

    return (
        <SidebarProvider>
            <AppSidebar />
            <SidebarInset>
                <header className="flex h-16 items-center gap-2 px-4 border-b">
                    <SidebarTrigger />
                    <div className="flex items-center gap-2">
                        <Sparkles className="h-5 w-5 text-blue-600" />
                        <h1 className="text-lg font-semibold">Future Features</h1>
                    </div>
                </header>

                <div className="flex-1 p-6">
                    <div className="max-w-4xl mx-auto space-y-8">
                        {/* Hero Section */}
                        <div className="text-center space-y-4">
                            <div className="inline-flex items-center gap-2 bg-blue-50 text-blue-700 px-4 py-2 rounded-full text-sm font-medium">
                                <Clock className="h-4 w-4" />
                                Coming Soon
                            </div>
                            <h2 className="text-3xl font-bold text-gray-900">
                                Exciting Features on the Horizon
                            </h2>
                            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                                We're constantly working to improve your invoice processing experience.
                                Here's a sneak peek at what's coming next!
                            </p>
                        </div>

                        {/* Main Hover Card Feature */}
                        <div className="flex justify-center">
                            <HoverCard>
                                <HoverCardTrigger asChild>
                                    <Card className="w-80 cursor-pointer hover:shadow-lg transition-all duration-200 hover:scale-105 border-2 border-dashed border-blue-200 bg-gradient-to-br from-blue-50 to-indigo-50">
                                        <CardHeader className="text-center">
                                            <div className="mx-auto w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                                                <Sparkles className="h-8 w-8 text-blue-600" />
                                            </div>
                                            <CardTitle className="text-xl text-blue-900">
                                                New Feature Placeholder
                                            </CardTitle>
                                        </CardHeader>
                                        <CardContent className="text-center">
                                            <p className="text-gray-600">
                                                Hover to discover what's coming next!
                                            </p>
                                        </CardContent>
                                    </Card>
                                </HoverCardTrigger>
                                <HoverCardContent className="w-80" align="center">
                                    <div className="text-center space-y-3">
                                        <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full mx-auto flex items-center justify-center">
                                            <Clock className="h-6 w-6 text-white" />
                                        </div>
                                        <h3 className="font-semibold text-lg">Stay Tuned!</h3>
                                        <p className="text-gray-600">
                                            New features coming soon! We're working hard to bring you
                                            amazing new capabilities that will revolutionize your
                                            invoice processing workflow.
                                        </p>
                                        <div className="text-xs text-gray-500 font-medium">
                                            Expected: Q2 2024
                                        </div>
                                    </div>
                                </HoverCardContent>
                            </HoverCard>
                        </div>

                        {/* Feature Preview Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-12">
                            {upcomingFeatures.map((feature, index) => (
                                <HoverCard key={index}>
                                    <HoverCardTrigger asChild>
                                        <Card className="cursor-pointer hover:shadow-lg transition-all duration-200 hover:scale-[1.02] border border-gray-200">
                                            <CardHeader>
                                                <div className="flex items-start gap-3">
                                                    <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
                                                        <feature.icon className="h-5 w-5 text-gray-600" />
                                                    </div>
                                                    <div className="flex-1">
                                                        <CardTitle className="text-lg">{feature.title}</CardTitle>
                                                        <div className="inline-flex items-center gap-1 mt-2">
                                                            <div className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></div>
                                                            <span className="text-xs text-gray-500 font-medium">
                                                                {feature.status}
                                                            </span>
                                                        </div>
                                                    </div>
                                                </div>
                                            </CardHeader>
                                        </Card>
                                    </HoverCardTrigger>
                                    <HoverCardContent className="w-64" side="top">
                                        <div className="space-y-2">
                                            <h4 className="font-medium">{feature.title}</h4>
                                            <p className="text-sm text-gray-600">
                                                {feature.description}
                                            </p>
                                            <div className="text-xs text-gray-500 font-medium pt-1 border-t">
                                                Status: {feature.status}
                                            </div>
                                        </div>
                                    </HoverCardContent>
                                </HoverCard>
                            ))}
                        </div>

                        {/* Call to Action */}
                        <div className="text-center bg-gray-50 rounded-xl p-8 mt-12">
                            <h3 className="text-xl font-semibold mb-2">Have Ideas?</h3>
                            <p className="text-gray-600 mb-4">
                                We'd love to hear your suggestions for new features that would make
                                your invoice processing even better.
                            </p>
                            <div className="inline-flex items-center gap-2 text-sm text-blue-600 font-medium">
                                <span>Send us feedback</span>
                                <span>→</span>
                            </div>
                        </div>
                    </div>
                </div>
            </SidebarInset>
        </SidebarProvider>
    );
}