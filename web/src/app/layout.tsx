import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "JETSO TESTO — AI-Powered Quiz Generation from PDFs",
  description:
    "Upload any PDF document and generate intelligent, interactive quizzes using local AI vision models. Built with Next.js, Flask, and Ollama.",
  keywords: [
    "AI quiz generator",
    "PDF to quiz",
    "AI education",
    "Ollama",
    "vision model",
    "local AI",
  ],
  openGraph: {
    title: "JETSO TESTO — AI-Powered Quiz Generation",
    description:
      "Transform any PDF into an interactive quiz with AI-powered vision analysis.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-surface-0 text-white antialiased">
        {children}
      </body>
    </html>
  );
}
