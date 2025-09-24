import ClaudeTest from '@/components/claude_test/ClaudeTest';

export default function Home() {
    return (
        <main className="container mx-auto p-8">
            <h1 className="text-2xl font-bold mb-8">Invoice Processing with Claude</h1>
            <ClaudeTest />
        </main>
    );
}