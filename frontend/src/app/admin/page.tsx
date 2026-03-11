'use client'
import { useEffect, useState } from 'react'
import { Users, BookOpen, BarChart2, Brain, DollarSign, Loader2, Shield } from 'lucide-react'

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface AdminStats {
  users: { total: number; by_tier: Record<string, number> }
  content: { total_chapters: number; free_chapters: number; premium_chapters: number; total_completions: number }
  quizzes: { total_submissions: number }
  hybrid_intelligence: { total_requests: number; total_cost_usd: number }
  revenue: { estimated_monthly_usd: number; premium_subscribers: number; pro_subscribers: number; team_subscribers: number }
}

export default function AdminPage() {
  const [stats, setStats] = useState<AdminStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch(`${BASE_URL}/admin/stats`)
      .then(r => r.json())
      .then(setStats)
      .catch(() => setError('Could not load admin stats. Is the backend running?'))
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

  if (!stats) return null

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">

      {/* Header */}
      <div className="mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gray-100 text-gray-700 text-sm font-medium mb-3">
          <Shield size={14} /> Phase 3 — Admin Panel
        </div>
        <h1 className="text-3xl font-bold text-gray-900">Platform Admin</h1>
        <p className="text-gray-500 mt-1">Real-time statistics for Course Companion FTE.</p>
      </div>

      {/* Top KPIs */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <KPI icon={<Users size={20} className="text-brand-500" />} value={String(stats.users.total)} label="Total Users" bg="bg-brand-50" />
        <KPI icon={<BookOpen size={20} className="text-green-500" />} value={String(stats.content.total_completions)} label="Chapter Completions" bg="bg-green-50" />
        <KPI icon={<BarChart2 size={20} className="text-amber-500" />} value={String(stats.quizzes.total_submissions)} label="Quiz Submissions" bg="bg-amber-50" />
        <KPI icon={<Brain size={20} className="text-purple-500" />} value={String(stats.hybrid_intelligence.total_requests)} label="AI Requests" bg="bg-purple-50" />
      </div>

      <div className="grid md:grid-cols-2 gap-6 mb-8">

        {/* User tier breakdown */}
        <div className="card p-6">
          <h2 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Users size={18} className="text-brand-500" /> Users by Tier
          </h2>
          <div className="space-y-3">
            {[
              { tier: 'free', label: 'Free', color: 'bg-gray-400', textColor: 'text-gray-700' },
              { tier: 'premium', label: 'Premium ($9.99/mo)', color: 'bg-blue-500', textColor: 'text-blue-700' },
              { tier: 'pro', label: 'Pro ($19.99/mo)', color: 'bg-amber-500', textColor: 'text-amber-700' },
              { tier: 'team', label: 'Team ($49.99/mo)', color: 'bg-purple-500', textColor: 'text-purple-700' },
            ].map(({ tier, label, color, textColor }) => {
              const count = stats.users.by_tier[tier] ?? 0
              const pct = stats.users.total > 0 ? Math.round((count / stats.users.total) * 100) : 0
              return (
                <div key={tier}>
                  <div className="flex items-center justify-between text-sm mb-1">
                    <span className={`font-medium ${textColor}`}>{label}</span>
                    <span className="text-gray-500">{count} users ({pct}%)</span>
                  </div>
                  <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                    <div className={`h-full rounded-full ${color} transition-all duration-700`} style={{ width: `${pct}%` }} />
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        {/* Revenue & Hybrid */}
        <div className="flex flex-col gap-4">
          {/* Revenue */}
          <div className="card p-6">
            <h2 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <DollarSign size={18} className="text-green-500" /> Revenue Estimate
            </h2>
            <div className="text-3xl font-bold text-green-700 mb-1">
              ${stats.revenue.estimated_monthly_usd.toFixed(2)}
            </div>
            <p className="text-xs text-gray-500 mb-4">Estimated monthly recurring revenue</p>
            <div className="space-y-1 text-sm text-gray-600">
              <div className="flex justify-between"><span>Premium × {stats.revenue.premium_subscribers}</span><span>${(stats.revenue.premium_subscribers * 9.99).toFixed(2)}</span></div>
              <div className="flex justify-between"><span>Pro × {stats.revenue.pro_subscribers}</span><span>${(stats.revenue.pro_subscribers * 19.99).toFixed(2)}</span></div>
              <div className="flex justify-between"><span>Team × {stats.revenue.team_subscribers}</span><span>${(stats.revenue.team_subscribers * 49.99).toFixed(2)}</span></div>
            </div>
          </div>

          {/* Hybrid AI usage */}
          <div className="card p-6">
            <h2 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
              <Brain size={18} className="text-purple-500" /> Hybrid AI Usage
            </h2>
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-purple-50 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-purple-700">{stats.hybrid_intelligence.total_requests}</div>
                <div className="text-xs text-purple-600 mt-1">Total Requests</div>
              </div>
              <div className="bg-green-50 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-green-700">${stats.hybrid_intelligence.total_cost_usd.toFixed(4)}</div>
                <div className="text-xs text-green-600 mt-1">Total LLM Cost</div>
              </div>
            </div>
            <p className="text-xs text-gray-400 mt-3">
              Phase 2 hybrid features (Assessment + Synthesis) — Pro tier only
            </p>
          </div>
        </div>
      </div>

      {/* Content stats */}
      <div className="card p-6">
        <h2 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <BookOpen size={18} className="text-brand-500" /> Content Statistics
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'Total Chapters', value: stats.content.total_chapters },
            { label: 'Free Chapters', value: stats.content.free_chapters },
            { label: 'Premium Chapters', value: stats.content.premium_chapters },
            { label: 'Total Completions', value: stats.content.total_completions },
          ].map(({ label, value }) => (
            <div key={label} className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">{value}</div>
              <div className="text-xs text-gray-500 mt-1">{label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Architecture note */}
      <div className="mt-6 card p-4 bg-blue-50 border-blue-200">
        <p className="text-blue-800 text-sm">
          <strong>Phase 3 Architecture:</strong> This admin panel uses <code className="bg-blue-100 px-1 rounded">GET /admin/stats</code> —
          a purely deterministic aggregation endpoint. Zero LLM calls. Phase 1 routes remain Zero-Backend-LLM.
          Phase 2 hybrid features (/hybrid/*) are Pro-gated with full cost tracking.
        </p>
      </div>
    </div>
  )
}

function KPI({ icon, value, label, bg }: { icon: React.ReactNode; value: string; label: string; bg: string }) {
  return (
    <div className={`card p-4 ${bg}`}>
      <div className="flex items-center gap-2 mb-1">{icon}</div>
      <div className="text-2xl font-bold text-gray-900">{value}</div>
      <div className="text-xs text-gray-500 mt-0.5">{label}</div>
    </div>
  )
}
