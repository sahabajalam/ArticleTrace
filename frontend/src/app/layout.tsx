import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const inter = Inter({ variable: "--font-inter", subsets: ["latin"] });
const mono = JetBrains_Mono({ variable: "--font-mono", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "ArticleTrace",
  description:
    "Static compliance scanner for AI codebases — every finding traced from a line of code to a cited EU AI Act or GDPR article.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body
        suppressHydrationWarning
        className={`${inter.variable} ${mono.variable} min-h-screen bg-white text-slate-900 antialiased`}
      >
        {/* One header, no sidebar. Two screens do not need navigation
            furniture — the product is the findings, not the chrome. */}
        <header className="border-b border-slate-200">
          <div className="mx-auto flex max-w-5xl items-baseline gap-3 px-6 py-4">
            <Link href="/" className="text-[15px] font-semibold tracking-tight">
              ArticleTrace
            </Link>
            <span className="text-[13px] text-slate-500">
              code → article, with evidence
            </span>
          </div>
        </header>
        <main className="mx-auto max-w-5xl px-6 py-8">{children}</main>
        <footer className="mx-auto max-w-5xl px-6 pb-10 pt-6 text-[12px] leading-relaxed text-slate-500">
          Static analysis, not legal advice. Findings indicate code patterns that
          commonly correspond to obligations; they cannot determine how a system
          is deployed, by whom, or for what purpose — which is frequently what
          decides its classification.
        </footer>
      </body>
    </html>
  );
}
