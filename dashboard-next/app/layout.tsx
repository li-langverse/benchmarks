import type { Metadata } from "next";
import "./globals.css";
import { Header } from "@/components/shell/header";

export const metadata: Metadata = {
  title: "Li Benchmarks",
  description: "Li-langverse performance, security, and correctness dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Header />
        {children}
      </body>
    </html>
  );
}
