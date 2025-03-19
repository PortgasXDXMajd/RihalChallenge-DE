import { ThemeProvider } from '@/context/ThemeProvider';

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="font-mono">
      <ThemeProvider>
        <div className="flex h-screen flex-col">{children}</div>
      </ThemeProvider>
    </div>
  );
}
