import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AI Job Hunt | Land Your Dream AI/ML Job",
  description: "AI-powered job search and auto-apply platform for ML Engineers, Data Scientists, and AI Researchers in Europe & Switzerland",
  keywords: ["AI jobs", "ML jobs", "machine learning careers", "Europe tech jobs", "Switzerland jobs", "auto-apply jobs"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
