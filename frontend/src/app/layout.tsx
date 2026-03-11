import type { Metadata } from 'next'
import './globals.css'
import Navbar from '@/components/layout/Navbar'

export const metadata: Metadata = {
  title: 'Course Companion FTE — AI Agent Development',
  description: 'Your 24/7 AI tutor for the AI Agent Development course. Learn Claude SDK, MCP, Agent Skills, and A2A Protocol.',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-1">{children}</main>
        <footer className="border-t border-gray-200 py-6 mt-12">
          <div className="max-w-5xl mx-auto px-4 text-center text-sm text-gray-500">
            Course Companion FTE · Panaversity Agent Factory Hackathon IV · Phase 1 + 2 + 3 Complete
          </div>
        </footer>
      </body>
    </html>
  )
}
