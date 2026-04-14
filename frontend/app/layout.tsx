import type { Metadata } from "next";
import { Toaster } from "sonner";

import AppShell from "@/components/layout/AppShell/AppShell";

import "./globals.css";

export const metadata: Metadata = {
  title: "Personal Health OS",
  description: "AI-powered health assistant gateway",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AppShell>{children}</AppShell>
        <Toaster richColors position="top-right" />
      </body>
    </html>
  );
}
