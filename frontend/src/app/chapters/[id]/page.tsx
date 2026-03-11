'use client'
import { useEffect, useState, useCallback } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import {
  ChevronLeft, ChevronRight, BookOpen, CheckCircle,
  Lock, AlertCircle, Loader2
} from 'lucide-react'
import {
  getChapter, getNextChapter, getPrevChapter,
  markChapterComplete, checkAccess,
} from '@/lib/api'
import type { ChapterDetail, ChapterNavigation } from '@/types'
import { DEFAULT_USER_ID } from '@/lib/api'
import SimpleMarkdown from '@/components/ui/SimpleMarkdown'
import AssessmentPanel from '@/components/ui/AssessmentPanel'

export default function ChapterPage() {
  const { id } = useParams<{ id: string }>()
  const chapterId = Number(id)
  const router = useRouter()

  const [chapter, setChapter]     = useState<ChapterDetail | null>(null)
  const [nav, setNav]             = useState<{ next: ChapterNavigation | null; prev: ChapterNavigation | null }>({ next: null, prev: null })
  const [loading, setLoading]     = useState(true)
  const [error, setError]         = useState<string | null>(null)
  const [blocked, setBlocked]     = useState(false)
  const [completing, setCompleting] = useState(false)
  const [completed, setCompleted]  = useState(false)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    setBlocked(false)

    try {
      const access = await checkAccess(DEFAULT_USER_ID, `chapter_${chapterId}`)
      if (!access.access) {
        setBlocked(true)
        setLoading(false)
        return
      }

      const [ch, nextNav, prevNav] = await Promise.all([
        getChapter(chapterId, DEFAULT_USER_ID),
        getNextChapter(chapterId, DEFAULT_USER_ID),
        getPrevChapter(chapterId, DEFAULT_USER_ID),
      ])
      setChapter(ch)
      setNav({ next: nextNav, prev: prevNav })
    } catch (e: unknown) {
      const err = e as { status?: number }
      if (err?.status === 403) setBlocked(true)
      else if (err?.status === 404) setError('Chapter not found.')
      else setError('Could not load chapter. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }, [chapterId])

  useEffect(() => { load() }, [load])

  async function handleComplete() {
    setCompleting(true)
    try {
      await markChapterComplete(DEFAULT_USER_ID, chapterId)
      setCompleted(true)
    } catch { /* ignore */ } finally {
      setCompleting(false)
    }
  }

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <Loader2 className="animate-spin text-brand-500" size={32} />
    </div>
  )

  if (blocked) return (
    <div className="max-w-2xl mx-auto px-4 py-20 text-center">
      <Lock size={48} className="text-amber-400 mx-auto mb-4" />
      <h2 className="text-2xl font-bold text-gray-900 mb-2">Premium Chapter</h2>
      <p className="text-gray-500 mb-6">
        This chapter requires a Premium subscription. Upgrade to access all 5 chapters.
      </p>
      <Link href="/chapters" className="btn-secondary">← Back to Chapters</Link>
    </div>
  )

  if (error) return (
    <div className="max-w-2xl mx-auto px-4 py-20 text-center">
      <AlertCircle size={40} className="text-red-400 mx-auto mb-4" />
      <p className="text-red-600 mb-4">{error}</p>
      <Link href="/chapters" className="btn-secondary">← Back to Chapters</Link>
    </div>
  )

  if (!chapter) return null

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      {/* Breadcrumb */}
      <div className="flex items-center gap-2 text-sm text-gray-500 mb-6">
        <Link href="/chapters" className="hover:text-brand-600 transition-colors">Chapters</Link>
        <ChevronRight size={14} />
        <span className="text-gray-700 font-medium">{chapter.title}</span>
      </div>

      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-sm font-medium text-brand-600 bg-brand-50 px-2 py-0.5 rounded">
            Chapter {chapter.order_index} of {chapter.total_chapters}
          </span>
          <span className={chapter.tier === 'free' ? 'badge-free' : 'badge-premium'}>
            {chapter.tier}
          </span>
        </div>
        <h1 className="text-3xl font-bold text-gray-900">{chapter.title}</h1>
        <p className="text-sm text-gray-400 mt-1">{chapter.word_count} words</p>
      </div>

      {/* Chapter body */}
      <div className="card p-6 md:p-8 mb-6">
        <SimpleMarkdown content={chapter.body} />
      </div>

      {/* Phase 2 — AI Assessment Panel */}
      <AssessmentPanel chapterId={chapterId} chapterTitle={chapter.title} />

      {/* Actions */}
      <div className="flex flex-wrap items-center gap-3 mb-8">
        {!completed ? (
          <button
            onClick={handleComplete}
            disabled={completing}
            className="btn-primary"
          >
            {completing
              ? <Loader2 size={16} className="animate-spin" />
              : <CheckCircle size={16} />
            }
            Mark as Complete
          </button>
        ) : (
          <span className="flex items-center gap-2 text-green-600 font-medium text-sm">
            <CheckCircle size={16} /> Chapter completed! 🎉
          </span>
        )}

        {chapter.has_quiz && (
          <Link href={`/chapters/${chapterId}/quiz`} className="btn-secondary">
            <BookOpen size={16} /> Take Quiz
          </Link>
        )}
      </div>

      {/* Navigation */}
      <div className="flex items-center justify-between gap-4">
        {!nav.prev?.is_boundary && nav.prev?.target ? (
          <Link
            href={`/chapters/${nav.prev.target.id}`}
            className="btn-secondary"
          >
            <ChevronLeft size={16} />
            <span className="hidden sm:inline">{nav.prev.target.title}</span>
            <span className="sm:hidden">Previous</span>
          </Link>
        ) : <div />}

        {!nav.next?.is_boundary && nav.next?.target ? (
          <Link
            href={`/chapters/${nav.next.target.id}`}
            className="btn-primary ml-auto"
          >
            <span className="hidden sm:inline">{nav.next.target.title}</span>
            <span className="sm:hidden">Next</span>
            <ChevronRight size={16} />
          </Link>
        ) : (
          <div className="ml-auto text-sm text-gray-500 font-medium">
            🎓 End of course
          </div>
        )}
      </div>
    </div>
  )
}
