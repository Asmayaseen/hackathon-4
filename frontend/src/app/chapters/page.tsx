import { listChapters } from '@/lib/api'
import Link from 'next/link'
import { BookOpen, Lock, ChevronRight } from 'lucide-react'
import type { ChapterMeta } from '@/types'

export const revalidate = 60

export default async function ChaptersPage() {
  let data: { chapters: ChapterMeta[]; total: number } | null = null
  let error = ''

  try {
    data = await listChapters()
  } catch {
    error = 'Could not load chapters. Make sure the backend is running.'
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Course Chapters</h1>
        <p className="text-gray-500">AI Agent Development · {data?.total ?? 0} chapters</p>
      </div>

      {error && (
        <div className="card p-4 border-red-200 bg-red-50 text-red-700 text-sm mb-6">{error}</div>
      )}

      {data && (
        <div className="card divide-y divide-gray-100">
          {data.chapters.map((ch) => (
            <Link
              key={ch.id}
              href={`/chapters/${ch.id}`}
              className="flex items-center gap-4 px-5 py-4 hover:bg-gray-50 transition-colors group"
            >
              {/* Chapter number */}
              <span className="w-9 h-9 rounded-full bg-brand-100 text-brand-700 font-bold text-sm flex items-center justify-center shrink-0">
                {ch.order_index}
              </span>

              {/* Info */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-0.5">
                  <span className="font-medium text-gray-900 group-hover:text-brand-700 transition-colors">
                    {ch.title}
                  </span>
                  {ch.tier === 'premium' && (
                    <Lock size={13} className="text-amber-500 shrink-0" />
                  )}
                </div>
                {ch.summary && (
                  <p className="text-sm text-gray-500 truncate">{ch.summary}</p>
                )}
              </div>

              {/* Right */}
              <div className="flex items-center gap-3 shrink-0">
                <span className={ch.tier === 'free' ? 'badge-free' : 'badge-premium'}>
                  {ch.tier === 'free' ? 'Free' : 'Premium'}
                </span>
                {ch.has_quiz && (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-blue-50 text-blue-700">
                    <BookOpen size={11} /> Quiz
                  </span>
                )}
                <ChevronRight size={16} className="text-gray-400 group-hover:text-brand-500 transition-colors" />
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
