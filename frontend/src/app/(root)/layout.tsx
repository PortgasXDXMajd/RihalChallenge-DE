export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="font-mono">
      <div className="flex h-screen flex-col gap-5">{children}</div>
    </div>
  );
}
