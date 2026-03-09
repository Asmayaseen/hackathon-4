'use client'
import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import { BookOpen, CheckCircle, XCircle, Loader2, ChevronRight, AlertCircle } from 'lucide-react'
import { getQuizByChapter, submitQuiz } from '@/lib/api'
import { DEFAULT_USER_ID } from '@/lib/api'
import type { QuizResponse, QuizResult } from '@/types'
import clsx from 'clsx'

type Phase = 'loading' | 'error' | 'no_quiz' | 'taking' | 'result'

export default function QuizPage() {
  const { id } = useParams<{ id: string }>()
  const chapterId = Number(id)

  const [phase, setPhase]       = useState<Phase>('loading')
  const [quiz, setQuiz]         = useState<QuizResponse | null>(null)
  const [current, setCurrent]   = useState(0)           // current question index
  const [answers, setAnswers]   = useState<Record<string, string>>({})
  const [result, setResult]     = useState<QuizResult | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError]       = useState('')

  useEffect(() => {
    getQuizByChapter(chapterId, DEFAULT_USER_ID)
      .then((q) => {
        setQuiz(q)
        setPhase(q.no_quiz_available ? 'no_quiz' : 'taking')
      })
      .catch(() => {
        setError('Could not load quiz.')
        setPhase('error')
      })
  }, [chapterId])

  function selectAnswer(questionId: number, option: string) {
    setAnswers((prev) => ({ ...prev, [String(questionId)]: option }))
  }

  async function handleSubmit() {
    if (!quiz) return
    setSubmitting(true)
    try {
      const res = await submitQuiz(quiz.quiz_id, DEFAULT_USER_ID, answers)
      setResult(res)
      setPhase('result')
    } catch {
      setError('Submission failed. Try again.')
    } finally {
      setSubmitting(false)
    }
  }

  if (phase === 'loading') return (
    <div className="flex items-center justify-center h-64">
      <Loader2 className="animate-spin text-brand-500" size={32} />
    </div>
  )

  if (phase === 'error') return (
    <div className="max-w-xl mx-auto px-4 py-16 text-center">
      <AlertCircle size={40} className="text-red-400 mx-auto mb-4" />
      <p className="text-red-600 mb-4">{error}</p>
      <Link href={`/chapters/${chapterId}`} className="btn-secondary">← Back to Chapter</Link>
    </div>
  )

  if (phase === 'no_quiz') return (
    <div className="max-w-xl mx-auto px-4 py-16 text-center">
      <BookOpen size={40} className="text-gray-300 mx-auto mb-4" />
      <p className="text-gray-500 mb-4">No quiz available for this chapter yet.</p>
      <Link href={`/chapters/${chapterId}`} className="btn-secondary">← Back to Chapter</Link>
    </div>
  )

  // ── Result ──────────────────────────────────────────────────────────────────
  if (phase === 'result' && result) {
    const pct = result.percentage
    const colour = pct >= 80 ? 'text-green-600' : pct >= 60 ? 'text-amber-600' : 'text-red-600'
    const bg = pct >= 80 ? 'bg-green-50' : pct >= 60 ? 'bg-amber-50' : 'bg-red-50'

    return (
      <div className="max-w-2xl mx-auto px-4 py-8">
        <div className={`card p-8 text-center mb-6 ${bg}`}>
          <div className={`text-5xl font-bold mb-2 ${colour}`}>{result.score}/{result.max_score}</div>
          <div className={`text-xl font-semibold mb-1 ${colour}`}>{pct}%</div>
          <div className="text-lg text-gray-700 font-medium">
            {pct >= 80 ? '🌟 Excellent work!' : pct >= 60 ? '✅ You passed!' : '💪 Keep going!'}
          </div>
        </div>

        <h3 className="font-semibold text-gray-800 mb-3">Review</h3>
        <div className="space-y-3 mb-8">
          {result.results.map((r, idx) => (
            <div key={r.question_id} className={`card p-4 border-l-4 ${r.passed ? 'border-green-400' : 'border-red-400'}`}>
              <div className="flex items-start gap-3">
                {r.passed
                  ? <CheckCircle size={18} className="text-green-500 mt-0.5 shrink-0" />
                  : <XCircle size={18} className="text-red-500 mt-0.5 shrink-0" />
                }
                <div>
                  <div className="font-medium text-gray-800 text-sm mb-1">
                    Q{idx + 1} · Your answer: <span className={r.passed ? 'text-green-700' : 'text-red-700'}>{r.submitted_answer}</span>
                    {!r.passed && <span className="text-gray-500"> · Correct: <span className="text-green-700 font-semibold">{r.correct_answer}</span></span>}
                  </div>
                  {r.explanation && (
                    <p className="text-sm text-gray-600">{r.explanation}</p>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="flex flex-wrap gap-3">
          <Link href={`/chapters/${chapterId}`} className="btn-secondary">← Back to Chapter</Link>
          <button onClick={() => { setPhase('taking'); setCurrent(0); setAnswers({}); setResult(null) }} className="btn-primary">
            Try Again
          </button>
          <Link href="/progress" className="btn-secondary">
            <BookOpen size={16} /> My Progress
          </Link>
        </div>
      </div>
    )
  }

  // ── Taking quiz ─────────────────────────────────────────────────────────────
  if (!quiz) return null
  const q = quiz.questions[current]
  const totalQ = quiz.total_questions
  const answered = answers[String(q.id)]
  const allAnswered = quiz.questions.every((qq) => answers[String(qq.id)])

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-6">
        <Link href={`/chapters/${chapterId}`} className="text-sm text-gray-500 hover:text-brand-600 flex items-center gap-1 mb-3">
          ← Back to Chapter
        </Link>
        <h1 className="text-2xl font-bold text-gray-900 mb-1">{quiz.title}</h1>
        <div className="flex items-center gap-2 text-sm text-gray-500">
          <span>Question {current + 1} of {totalQ}</span>
          <span>·</span>
          <span>{Object.keys(answers).length}/{totalQ} answered</span>
        </div>
        {/* Progress bar */}
        <div className="mt-3 h-1.5 bg-gray-200 rounded-full overflow-hidden">
          <div
            className="h-full bg-brand-500 transition-all"
            style={{ width: `${(Object.keys(answers).length / totalQ) * 100}%` }}
          />
        </div>
      </div>

      {/* Question card */}
      <div className="card p-6 mb-4">
        <p className="text-lg font-medium text-gray-900 mb-5">
          {current + 1}. {q.question_text}
        </p>
        <div className="space-y-2">
          {Object.entries(q.options).map(([key, val]) => (
            <button
              key={key}
              onClick={() => selectAnswer(q.id, key)}
              className={clsx(
                'w-full text-left flex items-center gap-3 px-4 py-3 rounded-lg border-2 transition-all text-sm font-medium',
                answered === key
                  ? 'border-brand-500 bg-brand-50 text-brand-800'
                  : 'border-gray-200 bg-white text-gray-700 hover:border-brand-300 hover:bg-brand-50/40',
              )}
            >
              <span className={clsx(
                'w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold shrink-0',
                answered === key ? 'bg-brand-500 text-white' : 'bg-gray-100 text-gray-600',
              )}>
                {key}
              </span>
              {val}
            </button>
          ))}
        </div>
      </div>

      {/* Navigation */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => setCurrent((c) => Math.max(0, c - 1))}
          disabled={current === 0}
          className="btn-secondary"
        >
          ← Prev
        </button>

        {current < totalQ - 1 ? (
          <button
            onClick={() => setCurrent((c) => c + 1)}
            className="btn-primary"
          >
            Next <ChevronRight size={16} />
          </button>
        ) : (
          <button
            onClick={handleSubmit}
            disabled={!allAnswered || submitting}
            className="btn-primary"
          >
            {submitting
              ? <Loader2 size={16} className="animate-spin" />
              : <CheckCircle size={16} />
            }
            {allAnswered ? 'Submit Quiz' : `Answer all (${totalQ - Object.keys(answers).length} left)`}
          </button>
        )}
      </div>

      {/* Question dots */}
      <div className="flex flex-wrap gap-1.5 mt-5">
        {quiz.questions.map((qq, idx) => (
          <button
            key={qq.id}
            onClick={() => setCurrent(idx)}
            className={clsx(
              'w-7 h-7 rounded text-xs font-semibold transition-all',
              idx === current ? 'bg-brand-600 text-white' :
              answers[String(qq.id)] ? 'bg-brand-100 text-brand-700' :
              'bg-gray-100 text-gray-500 hover:bg-gray-200',
            )}
          >
            {idx + 1}
          </button>
        ))}
      </div>
    </div>
  )
}
