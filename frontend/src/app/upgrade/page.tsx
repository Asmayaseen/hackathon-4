import Link from 'next/link'
import { CheckCircle, Zap, BookOpen, Brain, Users, BarChart2, Sparkles } from 'lucide-react'

const TIERS = [
  {
    name: 'Free',
    price: '$0',
    period: 'forever',
    color: 'border-gray-200',
    badge: 'bg-gray-100 text-gray-700',
    btnClass: 'btn-secondary',
    btnLabel: 'Current Plan',
    btnHref: '/chapters',
    features: [
      'Chapters 1–3 (Free)',
      'Basic quizzes (15 questions)',
      'Progress tracking',
      'Full-text search',
      'ChatGPT App tutoring',
    ],
    notIncluded: ['Chapters 4–5', 'AI Assessment', 'Cross-Chapter Synthesis'],
  },
  {
    name: 'Premium',
    price: '$9.99',
    period: 'per month',
    color: 'border-blue-400',
    badge: 'bg-blue-100 text-blue-700',
    btnClass: 'btn-primary',
    btnLabel: 'Upgrade to Premium',
    btnHref: '#',
    highlight: false,
    features: [
      'All 5 chapters',
      'All 25 quiz questions',
      'Progress tracking & streaks',
      'Full-text search',
      'ChatGPT App tutoring',
    ],
    notIncluded: ['AI Assessment (Pro)', 'Cross-Chapter Synthesis (Pro)'],
  },
  {
    name: 'Pro',
    price: '$19.99',
    period: 'per month',
    color: 'border-amber-400 ring-2 ring-amber-300',
    badge: 'bg-amber-100 text-amber-700',
    btnClass: 'bg-amber-500 hover:bg-amber-600 text-white inline-flex items-center gap-2 px-4 py-2 rounded-lg font-medium text-sm transition-colors',
    btnLabel: 'Upgrade to Pro',
    btnHref: '#',
    highlight: true,
    features: [
      'Everything in Premium',
      '🤖 AI-Graded Assessments (Claude Sonnet)',
      '✨ Cross-Chapter Synthesis (Claude Sonnet)',
      'Cost transparency per request',
      'Priority support',
    ],
    notIncluded: [],
  },
  {
    name: 'Team',
    price: '$49.99',
    period: 'per month',
    color: 'border-purple-400',
    badge: 'bg-purple-100 text-purple-700',
    btnClass: 'btn-secondary border-purple-300',
    btnLabel: 'Contact Sales',
    btnHref: 'mailto:team@course-companion.example.com',
    features: [
      'Everything in Pro',
      'Up to 10 seats',
      'Team analytics dashboard',
      'Admin panel access',
      'Custom onboarding',
    ],
    notIncluded: [],
  },
]

export default function UpgradePage() {
  return (
    <div className="max-w-5xl mx-auto px-4 py-12">

      {/* Header */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-50 text-brand-700 text-sm font-medium mb-4">
          <Zap size={14} /> Phase 3 — Pricing
        </div>
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Choose Your Learning Plan
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Start free. Upgrade when you need AI-powered features.
          All plans include 24/7 access to the Course Companion FTE.
        </p>
      </div>

      {/* Pricing cards */}
      <div className="grid md:grid-cols-4 gap-4 mb-12">
        {TIERS.map((tier) => (
          <div
            key={tier.name}
            className={`card p-5 border-2 ${tier.color} flex flex-col ${tier.highlight ? 'relative' : ''}`}
          >
            {tier.highlight && (
              <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-amber-500 text-white text-xs font-bold px-3 py-1 rounded-full whitespace-nowrap">
                Most Popular
              </div>
            )}
            <div className="mb-4">
              <span className={`inline-block px-2 py-0.5 rounded text-xs font-semibold mb-2 ${tier.badge}`}>
                {tier.name}
              </span>
              <div className="text-3xl font-bold text-gray-900">{tier.price}</div>
              <div className="text-xs text-gray-500">{tier.period}</div>
            </div>

            <ul className="space-y-2 mb-6 flex-1">
              {tier.features.map(f => (
                <li key={f} className="flex items-start gap-2 text-sm text-gray-700">
                  <CheckCircle size={14} className="text-green-500 mt-0.5 shrink-0" />
                  {f}
                </li>
              ))}
              {tier.notIncluded.map(f => (
                <li key={f} className="flex items-start gap-2 text-sm text-gray-400 line-through">
                  <span className="w-3.5 h-3.5 mt-0.5 shrink-0 text-center text-xs">✕</span>
                  {f}
                </li>
              ))}
            </ul>

            <Link href={tier.btnHref} className={`${tier.btnClass} justify-center text-center w-full py-2`}>
              {tier.btnLabel}
            </Link>
          </div>
        ))}
      </div>

      {/* Feature comparison */}
      <div className="card p-6 mb-8">
        <h2 className="text-xl font-bold text-gray-900 mb-6 text-center">Full Feature Comparison</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-2 pr-4 font-semibold text-gray-700">Feature</th>
                {['Free', 'Premium', 'Pro', 'Team'].map(t => (
                  <th key={t} className="text-center py-2 px-3 font-semibold text-gray-700">{t}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {[
                { feature: 'Chapters 1–3', free: '✅', premium: '✅', pro: '✅', team: '✅' },
                { feature: 'Chapters 4–5', free: '❌', premium: '✅', pro: '✅', team: '✅' },
                { feature: 'All 25 Quizzes', free: '❌', premium: '✅', pro: '✅', team: '✅' },
                { feature: 'Progress Tracking', free: '✅', premium: '✅', pro: '✅', team: '✅' },
                { feature: 'Full-Text Search', free: '✅', premium: '✅', pro: '✅', team: '✅' },
                { feature: 'AI Assessment (Claude)', free: '❌', premium: '❌', pro: '✅', team: '✅' },
                { feature: 'Cross-Chapter Synthesis', free: '❌', premium: '❌', pro: '✅', team: '✅' },
                { feature: 'LMS Dashboard', free: '✅', premium: '✅', pro: '✅', team: '✅' },
                { feature: 'Admin Panel', free: '❌', premium: '❌', pro: '❌', team: '✅' },
                { feature: 'Team Seats', free: '1', premium: '1', pro: '1', team: 'Up to 10' },
              ].map(row => (
                <tr key={row.feature}>
                  <td className="py-2.5 pr-4 text-gray-700 font-medium">{row.feature}</td>
                  <td className="py-2.5 px-3 text-center text-gray-600">{row.free}</td>
                  <td className="py-2.5 px-3 text-center text-gray-600">{row.premium}</td>
                  <td className="py-2.5 px-3 text-center text-amber-700 font-medium">{row.pro}</td>
                  <td className="py-2.5 px-3 text-center text-purple-700">{row.team}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Cost comparison */}
      <div className="card p-6 bg-gradient-to-r from-brand-50 to-amber-50 border-brand-200">
        <h2 className="text-lg font-bold text-gray-900 mb-4 text-center">
          Why Course Companion FTE?
        </h2>
        <div className="grid md:grid-cols-3 gap-4 text-center">
          {[
            { icon: <BookOpen size={24} className="text-brand-500" />, title: '168 hrs/week', desc: 'Available 24/7, never tired' },
            { icon: <Brain size={24} className="text-purple-500" />, title: '$0.004/session', desc: 'vs $50+ for human tutoring' },
            { icon: <Sparkles size={24} className="text-amber-500" />, title: '99%+ Consistent', desc: 'Deterministic Phase 1 backend' },
          ].map(({ icon, title, desc }) => (
            <div key={title} className="flex flex-col items-center gap-2">
              {icon}
              <div className="font-bold text-gray-900">{title}</div>
              <div className="text-sm text-gray-600">{desc}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
