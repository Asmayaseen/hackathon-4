import type {
  AccessCheck,
  ChapterDetail,
  ChapterListResponse,
  ChapterNavigation,
  QuizResponse,
  QuizResult,
  SearchResponse,
  UserProgress,
} from '@/types'

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const DEFAULT_USER_ID = 'web_user_001'

async function apiFetch<T>(
  path: string,
  options: RequestInit = {},
  userId: string = DEFAULT_USER_ID,
): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'X-User-ID': userId,
    ...(options.headers as Record<string, string>),
  }

  const res = await fetch(`${BASE_URL}${path}`, { ...options, headers })

  if (!res.ok) {
    const err = await res.json().catch(() => ({ message: res.statusText }))
    throw { status: res.status, detail: err.detail || err }
  }

  return res.json() as Promise<T>
}

// ─── Chapters ────────────────────────────────────────────────────────────────

export async function listChapters(userId?: string): Promise<ChapterListResponse> {
  return apiFetch('/chapters', {}, userId)
}

export async function getChapter(id: number, userId?: string): Promise<ChapterDetail> {
  return apiFetch(`/chapters/${id}`, {}, userId)
}

export async function getNextChapter(id: number, userId?: string): Promise<ChapterNavigation> {
  return apiFetch(`/chapters/${id}/next`, {}, userId)
}

export async function getPrevChapter(id: number, userId?: string): Promise<ChapterNavigation> {
  return apiFetch(`/chapters/${id}/previous`, {}, userId)
}

// ─── Search ───────────────────────────────────────────────────────────────────

export async function searchContent(
  query: string,
  limit = 5,
  userId?: string,
): Promise<SearchResponse> {
  const params = new URLSearchParams({ q: query, limit: String(limit) })
  return apiFetch(`/search?${params}`, {}, userId)
}

// ─── Quizzes ──────────────────────────────────────────────────────────────────

export async function getQuizByChapter(chapterId: number, userId?: string): Promise<QuizResponse> {
  return apiFetch(`/quizzes/chapter/${chapterId}`, {}, userId)
}

export async function submitQuiz(
  quizId: number,
  userId: string,
  answers: Record<string, string>,
): Promise<QuizResult> {
  return apiFetch(`/quizzes/${quizId}/submit`, {
    method: 'POST',
    body: JSON.stringify({ user_id: userId, answers }),
  })
}

// ─── Progress ─────────────────────────────────────────────────────────────────

export async function getUserProgress(userId: string): Promise<UserProgress> {
  return apiFetch(`/progress/${userId}`, {}, userId)
}

export async function markChapterComplete(
  userId: string,
  chapterId: number,
): Promise<UserProgress> {
  return apiFetch(`/progress/${userId}/chapters/${chapterId}`, {
    method: 'PUT',
    body: JSON.stringify({ completed: true }),
  })
}

// ─── Phase 2 Hybrid Intelligence ─────────────────────────────────────────────

export async function assessAnswer(
  chapterId: number,
  question: string,
  studentAnswer: string,
  userId?: string,
) {
  return apiFetch('/hybrid/assess', {
    method: 'POST',
    body: JSON.stringify({ chapter_id: chapterId, question, student_answer: studentAnswer }),
  }, userId)
}

export async function synthesizeChapters(
  chapterIds: number[],
  focusQuestion?: string,
  userId?: string,
) {
  return apiFetch('/hybrid/synthesize', {
    method: 'POST',
    body: JSON.stringify({ chapter_ids: chapterIds, focus_question: focusQuestion }),
  }, userId)
}

export async function getHybridUsage(userId: string) {
  return apiFetch(`/hybrid/usage/${userId}`, {}, userId)
}

// ─── Access ───────────────────────────────────────────────────────────────────

export async function checkAccess(
  userId: string,
  resource: string,
): Promise<AccessCheck> {
  const params = new URLSearchParams({ user_id: userId, resource })
  return apiFetch(`/access/check?${params}`, {}, userId)
}
