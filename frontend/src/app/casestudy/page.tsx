import {
    Card,
    CardAction,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"




export default function Page() {
    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">Case Study</h1>
                    <p className="text-gray-600 mt-2">AI driven invoice processing</p>
                </div>

                {/* Cards Container */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {/* Example Card - Replace with your actual cards */}
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                        <h3 className="text-lg font-medium text-gray-900 mb-2">Card Title</h3>
                        <p className="text-gray-600">Card content goes here</p>
                    </div>


                    <Card>
                        <CardHeader>
                            <CardTitle>Card Title</CardTitle>
                            <CardDescription>Card Description</CardDescription>
                            <CardAction>Card Action</CardAction>
                        </CardHeader>
                        <CardContent>
                            <p>Card Content</p>
                        </CardContent>
                        <CardFooter>
                            <p>Card Footer</p>
                        </CardFooter>
                    </Card>

                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                        <h3 className="text-lg font-medium text-gray-900 mb-2">Another Card</h3>
                        <p className="text-gray-600">More card content here</p>
                    </div>

                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                        <h3 className="text-lg font-medium text-gray-900 mb-2">Third Card</h3>
                        <p className="text-gray-600">Even more content</p>
                    </div>

                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                        <h3 className="text-lg font-medium text-gray-900 mb-2">Third Card</h3>
                        <p className="text-gray-600">Even more content</p>
                    </div>

                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                        <h3 className="text-lg font-medium text-gray-900 mb-2">Another Card</h3>
                        <p className="text-gray-600">More card content here</p>
                    </div>

                </div>
            </div>
        </div>
    );
}