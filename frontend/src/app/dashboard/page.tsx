'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import {
  BookOpen, BarChart2, Flame, Trophy, Sparkles,
  Search, Zap, ChevronRight, Loader2, CheckCircle
} from 'lucide-react'
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

export default function DashboardPage() {
  const [progress, setProgress] = useState<UserProgress | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getUserProgress(DEFAULT_USER_ID)
      .then(setProgress)
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <Loader2 className="animate-spin text-brand-500" size={32} />
    </div>
  )

  const pct = progress?.course_completion_pct ?? 0
  const completed = progress?.completed_chapters ?? []
  const scores = progress?.quiz_scores ?? {}
  const nextChapter = CHAPTERS.find(ch => !completed.includes(ch.id))

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">

      {/* Header */}
      <div className="mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-50 text-brand-700 text-sm font-medium mb-3">
          <Zap size={14} /> Phase 3 — Full LMS Dashboard
        </div>
        <h1 className="text-3xl font-bold text-gray-900">Learning Dashboard</h1>
        <p className="text-gray-500 mt-1">Your complete AI Agent Development journey at a glance.</p>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <StatCard icon={<BookOpen size={20} className="text-brand-500" />} value={`${completed.length}/5`} label="Chapters Done" bg="bg-brand-50" />
        <StatCard icon={<Flame size={20} className="text-orange-500" />} value={String(progress?.current_streak ?? 0)} label="Day Streak 🔥" bg="bg-orange-50" />
        <StatCard icon={<Trophy size={20} className="text-amber-500" />} value={String(progress?.longest_streak ?? 0)} label="Best Streak" bg="bg-amber-50" />
        <StatCard icon={<BarChart2 size={20} className="text-green-500" />} value={`${pct}%`} label="Completion" bg="bg-green-50" />
      </div>

      <div className="grid md:grid-cols-3 gap-6 mb-8">

        {/* Progress chart */}
        <div className="md:col-span-2 card p-6">
          <h2 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <BarChart2 size={18} className="text-brand-500" /> Quiz Scores by Chapter
          </h2>
          <div className="space-y-3">
            {CHAPTERS.map(ch => {
              const score = scores[String(ch.id)]
              const done = completed.includes(ch.id)
              const barPct = score !== undefined ? (score / 5) * 100 : 0
              return (
                <div key={ch.id}>
                  <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
                    <span className="flex items-center gap-1.5">
                      {done && <CheckCircle size={12} className="text-green-500" />}
                      Ch{ch.id}. {ch.title}
                    </span>
                    <span className="font-medium">
                      {score !== undefined ? `${score}/5` : done ? 'No quiz' : 'Not started'}
                    </span>
                  </div>
                  <div className="h-2.5 bg-gray-100 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all duration-700 ${
                        barPct >= 80 ? 'bg-green-500' : barPct >= 60 ? 'bg-amber-400' : barPct > 0 ? 'bg-red-400' : 'bg-gray-200'
                      }`}
                      style={{ width: `${barPct}%` }}
                    />
                  </div>
                </div>
              )
            })}
          </div>

          {/* Overall completion bar */}
          <div className="mt-6 pt-4 border-t border-gray-100">
            <div className="flex items-center justify-between text-sm mb-2">
              <span className="font-medium text-gray-700">Overall Course Progress</span>
              <span className="font-bold text-brand-700">{pct}%</span>
            </div>
            <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
              <div
                className="h-full bg-brand-500 rounded-full transition-all duration-700"
                style={{ width: `${pct}%` }}
              />
            </div>
            {pct === 100 && (
              <p className="mt-2 text-sm text-green-700 font-medium">🎓 Course complete! You're an AI Agent expert!</p>
            )}
          </div>
        </div>

        {/* Right panel */}
        <div className="flex flex-col gap-4">
          {/* Continue learning */}
          <div className="card p-5">
            <h2 className="font-semibold text-gray-900 mb-3 text-sm">Continue Learning</h2>
            {nextChapter ? (
              <Link
                href={`/chapters/${nextChapter.id}`}
                className="flex items-center justify-between gap-2 p-3 rounded-lg bg-brand-50 hover:bg-brand-100 transition-colors group"
              >
                <div>
                  <p className="text-xs text-brand-600 font-medium">Next up</p>
                  <p className="text-sm font-semibold text-brand-900 leading-tight mt-0.5">{nextChapter.title}</p>
                </div>
                <ChevronRight size={18} className="text-brand-500 group-hover:translate-x-0.5 transition-transform shrink-0" />
              </Link>
            ) : (
              <p className="text-sm text-green-600 font-medium">🎉 All chapters completed!</p>
            )}
          </div>

          {/* Quick actions */}
          <div className="card p-5">
            <h2 className="font-semibold text-gray-900 mb-3 text-sm">Quick Actions</h2>
            <div className="space-y-2">
              <Link href="/search" className="flex items-center gap-2 text-sm text-gray-600 hover:text-brand-700 py-1.5 transition-colors">
                <Search size={15} /> Search course content
              </Link>
              <Link href="/synthesis" className="flex items-center gap-2 text-sm text-gray-600 hover:text-brand-700 py-1.5 transition-colors">
                <Sparkles size={15} /> AI Synthesis <span className="text-xs px-1 py-0.5 rounded bg-amber-100 text-amber-700">Pro</span>
              </Link>
              <Link href="/progress" className="flex items-center gap-2 text-sm text-gray-600 hover:text-brand-700 py-1.5 transition-colors">
                <BarChart2 size={15} /> Full progress report
              </Link>
            </div>
          </div>

          {/* Tier badge */}
          <div className="card p-4">
            <p className="text-xs text-gray-500 mb-2">Current Plan</p>
            <div className="flex items-center justify-between">
              <span className={`text-sm font-bold ${progress?.tier === 'pro' ? 'text-amber-700' : progress?.tier === 'premium' ? 'text-blue-700' : 'text-gray-600'}`}>
                {(progress?.tier ?? 'free').charAt(0).toUpperCase() + (progress?.tier ?? 'free').slice(1)}
              </span>
              {progress?.tier === 'free' && (
                <Link href="/upgrade" className="text-xs text-brand-600 hover:underline font-medium">Upgrade →</Link>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Streak encouragement */}
      {(progress?.current_streak ?? 0) > 0 && (
        <div className="card p-4 bg-orange-50 border-orange-200">
          <p className="text-orange-800 font-medium text-sm">
            🔥 You are on a {progress?.current_streak}-day streak! Keep it going — log in tomorrow to maintain it!
          </p>
        </div>
      )}
    </div>
  )
}

function StatCard({ icon, value, label, bg }: { icon: React.ReactNode; value: string; label: string; bg: string }) {
  return (
    <div className={`card p-4 ${bg}`}>
      <div className="flex items-center gap-2 mb-1">{icon}</div>
      <div className="text-2xl font-bold text-gray-900">{value}</div>
      <div className="text-xs text-gray-500 mt-0.5">{label}</div>
    </div>
  )
}
