'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Flame, BookOpen, BarChart2, Trophy, Loader2, CheckCircle } from 'lucide-react'
import { getUserProgress } from '@/lib/api'
import { DEFAULT_USER_ID } from '@/lib/api'
import type { UserProgress } from '@/types'

const CHAPTERS = [
  { id: 1, title: 'Introduction to AI Agents',           tier: 'free' },
  { id: 2, title: 'Claude Agent SDK',                    tier: 'free' },
  { id: 3, title: 'Model Context Protocol (MCP)',         tier: 'free' },
  { id: 4, title: 'Agent Skills and SKILL.md',           tier: 'premium' },
  { id: 5, title: 'A2A Protocol and Multi-Agent Systems', tier: 'premium' },
]

export default function ProgressPage() {
  const [progress, setProgress] = useState<UserProgress | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    getUserProgress(DEFAULT_USER_ID)
      .then(setProgress)
      .catch(() => setError('Could not load progress. Is the backend running?'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <Loader2 className="animate-spin text-brand-500" size={32} />
    </div>
  )

  if (error) return (
    <div className="max-w-xl mx-auto px-4 py-16 text-center text-red-500">{error}</div>
  )

  if (!progress) return null

  const pct = progress.course_completion_pct

  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">My Progress</h1>

      {/* Top stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <Stat
          icon={<BookOpen size={20} className="text-brand-500" />}
          value={`${progress.completed_chapters.length}/5`}
          label="Chapters Done"
          bg="bg-brand-50"
        />
        <Stat
          icon={<Flame size={20} className="text-orange-500" />}
          value={String(progress.current_streak)}
          label="Day Streak 🔥"
          bg="bg-orange-50"
        />
        <Stat
          icon={<Trophy size={20} className="text-amber-500" />}
          value={String(progress.longest_streak)}
          label="Best Streak"
          bg="bg-amber-50"
        />
        <Stat
          icon={<BarChart2 size={20} className="text-green-500" />}
          value={`${progress.total_quiz_score}`}
          label="Total Quiz Score"
          bg="bg-green-50"
        />
      </div>

      {/* Overall progress bar */}
      <div className="card p-5 mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="font-semibold text-gray-800">Course Completion</span>
          <span className="text-brand-700 font-bold">{pct}%</span>
        </div>
        <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
          <div
            className="h-full bg-brand-500 transition-all duration-700"
            style={{ width: `${pct}%` }}
          />
        </div>
        {pct === 100 && (
          <p className="mt-2 text-sm text-green-700 font-medium">
            🎓 Course complete! You're an AI Agent expert!
          </p>
        )}
        {pct === 0 && (
          <p className="mt-2 text-sm text-gray-500">
            Start with <Link href="/chapters/1" className="text-brand-600 underline">Chapter 1</Link> to begin your journey!
          </p>
        )}
      </div>

      {/* Tier badge */}
      <div className="card p-4 mb-6 flex items-center justify-between">
        <span className="text-sm text-gray-600">Your current plan</span>
        <span className={progress.tier === 'free' ? 'badge-free text-sm px-3 py-1' : 'badge-premium text-sm px-3 py-1'}>
          {progress.tier.charAt(0).toUpperCase() + progress.tier.slice(1)}
        </span>
      </div>

      {/* Chapter breakdown */}
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Chapter Progress</h2>
      <div className="card divide-y divide-gray-100">
        {CHAPTERS.map((ch) => {
          const done = progress.completed_chapters.includes(ch.id)
          const score = progress.quiz_scores[String(ch.id)]
          return (
            <div key={ch.id} className="flex items-center gap-4 px-5 py-4">
              {done
                ? <CheckCircle size={20} className="text-green-500 shrink-0" />
                : <div className="w-5 h-5 rounded-full border-2 border-gray-300 shrink-0" />
              }
              <div className="flex-1 min-w-0">
                <p className={`font-medium text-sm truncate ${done ? 'text-gray-900' : 'text-gray-500'}`}>
                  Ch{ch.id}. {ch.title}
                </p>
                {score !== undefined && (
                  <p className="text-xs text-gray-400 mt-0.5">Quiz score: {score}/5</p>
                )}
              </div>
              <div className="flex items-center gap-2 shrink-0">
                <span className={ch.tier === 'free' ? 'badge-free' : 'badge-premium'}>
                  {ch.tier}
                </span>
                <Link href={`/chapters/${ch.id}`} className="text-xs text-brand-600 hover:underline">
                  {done ? 'Review' : 'Start'}
                </Link>
              </div>
            </div>
          )
        })}
      </div>

      {/* Streak encouragement */}
      {progress.current_streak > 0 && (
        <div className="mt-6 card p-4 bg-orange-50 border-orange-200">
          <p className="text-orange-800 font-medium text-sm">
            🔥 You're on a {progress.current_streak}-day streak! Keep it going — log in tomorrow to maintain it!
          </p>
        </div>
      )}
    </div>
  )
}

function Stat({ icon, value, label, bg }: { icon: React.ReactNode; value: string; label: string; bg: string }) {
  return (
    <div className={`card p-4 ${bg}`}>
      <div className="flex items-center gap-2 mb-1">{icon}</div>
      <div className="text-2xl font-bold text-gray-900">{value}</div>
      <div className="text-xs text-gray-500 mt-0.5">{label}</div>
    </div>
  )
}
