'use client';
import './globals.css';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" type="image/svg+xml" href="/logos/red_logo.svg" />
      </head>
      <body className={inter.className}>
        <div className="font-mono">
          {children}
        </div>
      </body>
    </html>
  );
}
