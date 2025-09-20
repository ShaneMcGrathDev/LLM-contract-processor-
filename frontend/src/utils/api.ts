//API Congifuration
//Note: You can expand later for the other HTTP methods (POST, PUT, DELETE, etc.)


const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export async function fetchData(endpoint: string) {
    const response = await fetch(`${API_BASE_URL}/api/${endpoint}`);
    if (!response.ok) {
        throw new Error('Failed to fetch data');
    }
    return response.json();
}