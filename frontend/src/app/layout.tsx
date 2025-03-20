'use client';
import './globals.css';

export default function Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html>
      <body>
        <div>
          {children}
        </div>
      </body>
    </html>
  );
}
