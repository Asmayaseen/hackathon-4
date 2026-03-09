import Link from 'next/link'
import { BookOpen, BarChart2, Zap, Shield, Clock, Users } from 'lucide-react'

const features = [
  { icon: BookOpen,  title: 'Content Delivery',   desc: '5 chapters on AI Agent Development, served verbatim from Cloudflare R2.' },
  { icon: Zap,       title: 'Grounded Q&A',        desc: 'Search course content and get answers backed exclusively by the material.' },
  { icon: Shield,    title: 'Rule-Based Quizzes',  desc: '5-question quizzes per chapter, graded by answer key — no LLM in the backend.' },
  { icon: BarChart2, title: 'Progress & Streaks',  desc: 'Track chapter completions, quiz scores, and daily learning streaks.' },
  { icon: Clock,     title: '24/7 Availability',   desc: '168 hours a week, unlimited concurrent students, 99%+ consistency.' },
  { icon: Users,     title: 'Freemium Gate',       desc: 'First 3 chapters free. Upgrade to Premium for all 5 chapters and quizzes.' },
]

export default function HomePage() {
  return (
    <div className="max-w-5xl mx-auto px-4 py-12">
      {/* Hero */}
      <div className="text-center mb-16">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-50 text-brand-700 text-sm font-medium mb-4">
          <Zap size={14} /> Zero-Backend-LLM · Phase 1
        </div>
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Your 24/7 AI Tutor for<br />
          <span className="text-brand-600">AI Agent Development</span>
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-8">
          Master Claude SDK, MCP, Agent Skills, and A2A Protocol at your own pace.
          Powered by the Agent Factory Architecture — at 99% less cost than human tutors.
        </p>
        <div className="flex justify-center gap-3 flex-wrap">
          <Link href="/chapters" className="btn-primary text-base px-6 py-3">
            <BookOpen size={18} /> Start Learning
          </Link>
          <Link href="/progress" className="btn-secondary text-base px-6 py-3">
            <BarChart2 size={18} /> My Progress
          </Link>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-16">
        {[
          { value: '5', label: 'Chapters' },
          { value: '25', label: 'Quiz Questions' },
          { value: '$0', label: 'LLM Cost (Backend)' },
          { value: '168h', label: 'Weekly Availability' },
        ].map(({ value, label }) => (
          <div key={label} className="card p-4 text-center">
            <div className="text-3xl font-bold text-brand-600">{value}</div>
            <div className="text-sm text-gray-500 mt-1">{label}</div>
          </div>
        ))}
      </div>

      {/* Features */}
      <h2 className="text-2xl font-bold text-gray-900 mb-6">What You Can Do</h2>
      <div className="grid md:grid-cols-3 gap-4 mb-16">
        {features.map(({ icon: Icon, title, desc }) => (
          <div key={title} className="card p-5">
            <div className="w-9 h-9 rounded-lg bg-brand-50 flex items-center justify-center mb-3">
              <Icon size={18} className="text-brand-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-1">{title}</h3>
            <p className="text-sm text-gray-600">{desc}</p>
          </div>
        ))}
      </div>

      {/* Course Outline */}
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Course Outline</h2>
      <div className="card divide-y divide-gray-100">
        {[
          { n: 1, title: 'Introduction to AI Agents',          tier: 'free' },
          { n: 2, title: 'Claude Agent SDK',                   tier: 'free' },
          { n: 3, title: 'Model Context Protocol (MCP)',        tier: 'free' },
          { n: 4, title: 'Agent Skills and SKILL.md',          tier: 'premium' },
          { n: 5, title: 'A2A Protocol and Multi-Agent Systems',tier: 'premium' },
        ].map(({ n, title, tier }) => (
          <Link
            key={n}
            href={`/chapters/${n}`}
            className="flex items-center gap-4 px-5 py-4 hover:bg-gray-50 transition-colors group"
          >
            <span className="w-8 h-8 rounded-full bg-brand-100 text-brand-700 text-sm font-bold flex items-center justify-center shrink-0">
              {n}
            </span>
            <span className="flex-1 font-medium text-gray-800 group-hover:text-brand-700 transition-colors">
              {title}
            </span>
            <span className={tier === 'free' ? 'badge-free' : 'badge-premium'}>
              {tier === 'free' ? 'Free' : 'Premium'}
            </span>
          </Link>
        ))}
      </div>
    </div>
  )
}
