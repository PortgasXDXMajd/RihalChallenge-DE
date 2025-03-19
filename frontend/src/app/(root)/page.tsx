'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import CrimeService from '@/services/CrimeService';

const Home = () => {
  const [data, setData] = useState<CrimeData[] | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const state = await CrimeService.get_state(); 
        setData(state);
      } catch (err) {
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  if (isLoading) {
    return (
      <div className="w-full h-full flex items-center justify-center">
        Loading...
      </div>
    );
  }

  return (
    <div className="w-full h-full p-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {data?.map((item:any, index:number) => (
          <Card 
            key={index}
            className="shadow-lg hover:shadow-xl transition-shadow duration-300"
          >
            <CardHeader>
              <CardTitle className="text-lg font-semibold text-gray-800">
                {item.metric}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <p className="text-2xl font-bold text-blue-600">
                  {item.result}
                </p>
                <p className="text-sm text-gray-600">
                  Value: {item.value}
                </p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default Home;