'use client'
import { useState } from 'react'
import { Search, Loader2, AlertCircle, BookOpen } from 'lucide-react'
import Link from 'next/link'
import { searchContent } from '@/lib/api'
import { DEFAULT_USER_ID } from '@/lib/api'
import type { SearchResponse } from '@/types'

export default function SearchPage() {
  const [query, setQuery]       = useState('')
  const [loading, setLoading]   = useState(false)
  const [result, setResult]     = useState<SearchResponse | null>(null)
  const [error, setError]       = useState('')

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault()
    if (!query.trim() || query.length < 2) return
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const res = await searchContent(query.trim(), 5, DEFAULT_USER_ID)
      setResult(res)
    } catch {
      setError('Search failed. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Search Course Content</h1>
        <p className="text-gray-500 text-sm">
          Search across all chapters you have access to. Results are grounded in course material only.
        </p>
      </div>

      {/* Search box */}
      <form onSubmit={handleSearch} className="flex gap-2 mb-8">
        <div className="flex-1 relative">
          <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g. What is an MCP server?"
            className="w-full pl-10 pr-4 py-2.5 rounded-lg border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400 focus:border-transparent"
            minLength={2}
            maxLength={500}
          />
        </div>
        <button type="submit" disabled={loading || query.length < 2} className="btn-primary px-5">
          {loading ? <Loader2 size={16} className="animate-spin" /> : <Search size={16} />}
          Search
        </button>
      </form>

      {/* Error */}
      {error && (
        <div className="flex items-center gap-2 text-red-600 text-sm mb-4">
          <AlertCircle size={16} /> {error}
        </div>
      )}

      {/* Results */}
      {result && (
        <div>
          {result.no_results ? (
            <div className="text-center py-12 text-gray-400">
              <Search size={36} className="mx-auto mb-3 opacity-50" />
              <p className="font-medium">No results for "{result.query}"</p>
              <p className="text-sm mt-1">This topic may not be covered in the course yet.</p>
            </div>
          ) : (
            <>
              <p className="text-sm text-gray-500 mb-4">
                {result.total} result{result.total !== 1 ? 's' : ''} for "<strong>{result.query}</strong>"
              </p>
              <div className="space-y-3">
                {result.sections.map((section) => (
                  <div key={section.id} className="card p-5">
                    <div className="flex items-center justify-between mb-2">
                      <Link
                        href={`/chapters/${section.chapter_id}`}
                        className="flex items-center gap-1.5 text-xs font-medium text-brand-700 hover:underline"
                      >
                        <BookOpen size={12} /> {section.chapter_title}
                      </Link>
                      <span className="text-xs text-gray-400">
                        {(section.relevance_score * 100).toFixed(0)}% match
                      </span>
                    </div>
                    <p className="text-sm text-gray-700 leading-relaxed line-clamp-4">
                      {section.text}
                    </p>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      )}

      {/* Hint when empty */}
      {!result && !loading && (
        <div className="text-center py-12 text-gray-300">
          <Search size={48} className="mx-auto mb-3" />
          <p className="text-gray-400 text-sm">Type a question to search course content</p>
          <div className="mt-4 flex flex-wrap justify-center gap-2">
            {['What is an AI agent?', 'How does MCP work?', 'What is the agent loop?'].map((q) => (
              <button
                key={q}
                onClick={() => setQuery(q)}
                className="text-xs px-3 py-1.5 rounded-full border border-gray-200 text-gray-500 hover:border-brand-300 hover:text-brand-600 transition-colors"
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
