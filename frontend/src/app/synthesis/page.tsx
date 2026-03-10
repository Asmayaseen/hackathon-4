'use client'
import { useState } from 'react'
import { Sparkles, Loader2, AlertCircle, BookOpen, Lock } from 'lucide-react'
import { synthesizeChapters } from '@/lib/api'
import { DEFAULT_USER_ID } from '@/lib/api'
import SimpleMarkdown from '@/components/ui/SimpleMarkdown'

const CHAPTERS = [
  { id: 1, title: 'Introduction to AI Agents' },
  { id: 2, title: 'Claude Agent SDK' },
  { id: 3, title: 'Model Context Protocol (MCP)' },
  { id: 4, title: 'Agent Skills and SKILL.md' },
  { id: 5, title: 'A2A Protocol and Multi-Agent Systems' },
]

export default function SynthesisPage() {
  const [selected, setSelected]     = useState<number[]>([])
  const [focus, setFocus]           = useState('')
  const [loading, setLoading]       = useState(false)
  const [result, setResult]         = useState<any>(null)
  const [error, setError]           = useState('')
  const [proError, setProError]     = useState(false)

  function toggleChapter(id: number) {
    setSelected(prev =>
      prev.includes(id) ? prev.filter(x => x !== id) : prev.length < 5 ? [...prev, id] : prev
    )
  }

  async function handleSynthesize() {
    if (selected.length < 2) return
    setLoading(true)
    setError('')
    setProError(false)
    setResult(null)
    try {
      const res = await synthesizeChapters(selected, focus || undefined, DEFAULT_USER_ID)
      setResult(res)
    } catch (err: any) {
      if (err?.status === 403) {
        setProError(true)
      } else if (err?.status === 503) {
        setError('Phase 2 hybrid features not configured yet. Add ANTHROPIC_API_KEY to backend.')
      } else {
        setError('Synthesis failed. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-2">
          <h1 className="text-3xl font-bold text-gray-900">Cross-Chapter Synthesis</h1>
          <span className="badge-premium text-xs px-2 py-1">Pro</span>
        </div>
        <p className="text-gray-500 text-sm">
          Select 2–5 chapters and Claude AI will generate a connected "big picture" explanation
          showing how concepts relate across chapters.
        </p>
      </div>

      {/* Pro gate notice */}
      {proError && (
        <div className="card p-5 bg-amber-50 border-amber-200 mb-6">
          <div className="flex items-center gap-3">
            <Lock size={20} className="text-amber-600 shrink-0" />
            <div>
              <p className="font-semibold text-amber-900">Pro Feature</p>
              <p className="text-sm text-amber-700 mt-1">
                Cross-Chapter Synthesis requires a Pro subscription ($19.99/month).
                Upgrade to unlock AI-powered synthesis and LLM-graded assessments.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Chapter selector */}
      <div className="card p-5 mb-5">
        <p className="text-sm font-medium text-gray-700 mb-3">
          Select chapters to synthesize ({selected.length}/5 selected, min 2):
        </p>
        <div className="space-y-2">
          {CHAPTERS.map(ch => (
            <button
              key={ch.id}
              onClick={() => toggleChapter(ch.id)}
              className={`w-full text-left flex items-center gap-3 px-4 py-3 rounded-lg border-2 transition-all text-sm
                ${selected.includes(ch.id)
                  ? 'border-brand-500 bg-brand-50 text-brand-800'
                  : 'border-gray-200 bg-white text-gray-700 hover:border-brand-300'
                }`}
            >
              <span className={`w-6 h-6 rounded flex items-center justify-center text-xs font-bold shrink-0
                ${selected.includes(ch.id) ? 'bg-brand-500 text-white' : 'bg-gray-100 text-gray-500'}`}>
                {ch.id}
              </span>
              {ch.title}
              {selected.includes(ch.id) && (
                <span className="ml-auto text-brand-500 text-xs font-semibold">✓</span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Focus question (optional) */}
      <div className="mb-5">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Focus question <span className="text-gray-400">(optional)</span>
        </label>
        <input
          type="text"
          value={focus}
          onChange={e => setFocus(e.target.value)}
          placeholder="e.g. How do MCP and Agent Skills work together?"
          className="w-full px-4 py-2.5 rounded-lg border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
          maxLength={300}
        />
      </div>

      {/* Action button */}
      <button
        onClick={handleSynthesize}
        disabled={selected.length < 2 || loading}
        className="btn-primary w-full justify-center py-3 mb-6"
      >
        {loading
          ? <><Loader2 size={16} className="animate-spin" /> Synthesizing with Claude AI...</>
          : <><Sparkles size={16} /> Generate Synthesis ({selected.length} chapters)</>
        }
      </button>

      {/* Error */}
      {error && (
        <div className="flex items-center gap-2 text-red-600 text-sm mb-4">
          <AlertCircle size={16} /> {error}
        </div>
      )}

      {/* Result */}
      {result && (
        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-gray-900 flex items-center gap-2">
              <Sparkles size={18} className="text-brand-500" /> AI Synthesis
            </h2>
            <div className="text-xs text-gray-400 text-right">
              <p>{result.tokens_used} tokens used</p>
              <p>~${Number(result.cost_usd).toFixed(4)} cost</p>
            </div>
          </div>

          <div className="flex flex-wrap gap-2 mb-4">
            {result.chapters_used?.map((title: string, i: number) => (
              <span key={i} className="flex items-center gap-1 text-xs px-2 py-1 bg-brand-50 text-brand-700 rounded-full border border-brand-200">
                <BookOpen size={10} /> {title}
              </span>
            ))}
          </div>

          <div className="border-t pt-4">
            <SimpleMarkdown content={result.synthesis} />
          </div>
        </div>
      )}

      {/* Empty state */}
      {!result && !loading && !proError && (
        <div className="text-center py-10 text-gray-300">
          <Sparkles size={48} className="mx-auto mb-3" />
          <p className="text-gray-400 text-sm">Select at least 2 chapters to generate a synthesis</p>
        </div>
      )}
    </div>
  )
}
