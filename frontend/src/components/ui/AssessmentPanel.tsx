'use client'
import { useState } from 'react'
import { Brain, Loader2, Lock, CheckCircle, AlertCircle } from 'lucide-react'
import { assessAnswer } from '@/lib/api'
import { DEFAULT_USER_ID } from '@/lib/api'

interface Props {
  chapterId: number
  chapterTitle: string
}

const SAMPLE_QUESTIONS: Record<number, string> = {
  1: 'Explain what an AI agent is and how it differs from a traditional program.',
  2: 'Describe how the Claude Agent SDK enables multi-turn conversations with tool use.',
  3: 'What is the Model Context Protocol and why is it important for AI agents?',
  4: 'Explain what a SKILL.md file is and how agent skills work.',
  5: 'How does the A2A Protocol enable multi-agent collaboration?',
}

export default function AssessmentPanel({ chapterId, chapterTitle }: Props) {
  const [answer, setAnswer]     = useState('')
  const [loading, setLoading]   = useState(false)
  const [result, setResult]     = useState<any>(null)
  const [error, setError]       = useState('')
  const [proError, setProError] = useState(false)

  const question = SAMPLE_QUESTIONS[chapterId] || `Explain the key concepts from ${chapterTitle}.`

  async function handleAssess() {
    if (answer.trim().length < 10) return
    setLoading(true)
    setError('')
    setProError(false)
    setResult(null)
    try {
      const res = await assessAnswer(chapterId, question, answer.trim(), DEFAULT_USER_ID)
      setResult(res)
    } catch (err: any) {
      if (err?.status === 403) setProError(true)
      else if (err?.status === 503) setError('Hybrid AI not configured (add ANTHROPIC_API_KEY).')
      else setError('Assessment failed. Try again.')
    } finally {
      setLoading(false)
    }
  }

  const scoreColor = result
    ? result.score >= 8 ? 'text-green-600' : result.score >= 6 ? 'text-amber-600' : 'text-red-600'
    : ''

  return (
    <div className="card p-5 mt-6 border-brand-200">
      <div className="flex items-center gap-2 mb-1">
        <Brain size={18} className="text-brand-600" />
        <h3 className="font-semibold text-gray-900">AI Assessment</h3>
        <span className="badge-premium text-xs px-2 py-0.5">Pro</span>
      </div>
      <p className="text-xs text-gray-500 mb-4">
        Write your answer in your own words — Claude AI will evaluate your understanding.
      </p>

      <div className="bg-brand-50 rounded-lg p-3 mb-3">
        <p className="text-sm font-medium text-brand-800">📝 {question}</p>
      </div>

      <textarea
        value={answer}
        onChange={e => setAnswer(e.target.value)}
        placeholder="Write your answer here (minimum 10 characters)..."
        rows={4}
        maxLength={1000}
        className="w-full px-3 py-2 rounded-lg border border-gray-300 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-brand-400 mb-3"
      />
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs text-gray-400">{answer.length}/1000 characters</span>
        <button
          onClick={handleAssess}
          disabled={answer.trim().length < 10 || loading}
          className="btn-primary text-sm px-4"
        >
          {loading ? <><Loader2 size={14} className="animate-spin" /> Evaluating...</> : <><Brain size={14} /> Assess My Answer</>}
        </button>
      </div>

      {/* Pro gate */}
      {proError && (
        <div className="flex items-start gap-2 p-3 bg-amber-50 rounded-lg border border-amber-200">
          <Lock size={16} className="text-amber-600 mt-0.5 shrink-0" />
          <div>
            <p className="text-sm font-medium text-amber-900">Pro Feature Required</p>
            <p className="text-xs text-amber-700 mt-0.5">AI Assessment requires Pro ($19.99/mo). Upgrade to unlock.</p>
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="flex items-center gap-2 text-red-600 text-xs">
          <AlertCircle size={14} /> {error}
        </div>
      )}

      {/* Result */}
      {result && (
        <div className="border-t pt-4 mt-2">
          <div className="flex items-center justify-between mb-3">
            <span className={`text-3xl font-bold ${scoreColor}`}>{result.score}/10</span>
            <span className="text-xs text-gray-400">~${Number(result.cost_usd).toFixed(4)} used</span>
          </div>
          <p className="text-sm text-gray-700 mb-3">{result.feedback}</p>

          {result.strengths?.length > 0 && (
            <div className="mb-2">
              <p className="text-xs font-semibold text-green-700 mb-1">✅ Strengths</p>
              <ul className="space-y-0.5">
                {result.strengths.map((s: string, i: number) => (
                  <li key={i} className="text-xs text-gray-600 flex items-start gap-1">
                    <CheckCircle size={10} className="text-green-500 mt-0.5 shrink-0" /> {s}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {result.improvements?.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-amber-700 mb-1">💡 Improvements</p>
              <ul className="space-y-0.5">
                {result.improvements.map((imp: string, i: number) => (
                  <li key={i} className="text-xs text-gray-600 flex items-start gap-1">
                    <span className="text-amber-500 mt-0.5 shrink-0">→</span> {imp}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
