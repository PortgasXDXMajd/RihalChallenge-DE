'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import CrimeService from '@/services/CrimeService';

interface CrimeData {
  metric: string;
  result: string | number;
  value: string | number;
}

const Home = () => {
  const [data, setData] = useState<CrimeData[] | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const state = await CrimeService.get_state();
        setData(state);
      } catch (err) {
        console.error('Error fetching crime data:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-lg font-medium text-gray-600 animate-pulse">
          Loading...
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      {/* Header Section */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">Crime Dashboard</h1>
          <p className="mt-1 text-sm text-gray-500">
            Real-time crime statistics and insights
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {data?.map((item, index) => (
            <Card
              key={index}
              className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 border border-gray-200"
            >
              <CardHeader className="border-b border-gray-100 pb-3">
                <CardTitle className="text-lg font-semibold text-gray-800 capitalize">
                  {item.metric.replace(/_/g, ' ')}
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-4">
                <div className="space-y-3">
                  <p className="text-3xl font-bold text-indigo-600">
                    {item.result}
                  </p>
                  <p className="text-sm text-gray-500">
                    <span className="font-medium">Value:</span> {item.value}
                  </p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </main>

      <footer className="bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <p className="text-sm text-gray-500 text-center">
            © {new Date().getFullYear()} Crime Dashboard. All rights reserved. | Designed by{' '}
            <span className="font-medium text-indigo-600">Grok (xAI)</span> <span className="font-medium text-indigo-600">I hate frontend...</span> 
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Home;