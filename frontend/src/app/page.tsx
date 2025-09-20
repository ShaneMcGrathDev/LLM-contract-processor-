'use client';

import { useEffect, useState } from 'react';
import { fetchData } from '@/utils/api';

export default function Home() {
  const [data, setData] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData('data')
      .then((response) => {
        setData(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error:', error);
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen p-8">
      <h1 className="text-4xl font-bold mb-8">Full Stack Template</h1>
      <div className="bg-gray-100 p-4 rounded">
        <h2 className="text-xl font-semibold mb-2">Backend Response:</h2>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <p>{data || 'No data received'}</p>
        )}
      </div>
    </div>
  );
}