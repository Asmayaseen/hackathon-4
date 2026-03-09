export interface ChapterMeta {
  id: number
  title: string
  order_index: number
  tier: 'free' | 'premium'
  has_quiz: boolean
  summary: string | null
}

export interface ChapterDetail extends ChapterMeta {
  body: string
  word_count: number
  total_chapters: number
}

export interface ChapterNavigation {
  current_chapter_id: number
  target: ChapterMeta | null
  is_boundary: boolean
  boundary_type: 'first' | 'last' | null
}

export interface ChapterListResponse {
  chapters: ChapterMeta[]
  total: number
}

export interface ContentSection {
  id: number
  chapter_id: number
  chapter_title: string
  text: string
  relevance_score: number
}

export interface SearchResponse {
  query: string
  total: number
  no_results: boolean
  sections: ContentSection[]
}

export interface QuizQuestion {
  id: number
  position: number
  question_text: string
  options: Record<string, string>
}

export interface QuizResponse {
  quiz_id: number
  chapter_id: number
  title: string
  questions: QuizQuestion[]
  total_questions: number
  no_quiz_available: boolean
}

export interface QuestionResult {
  question_id: number
  submitted_answer: string
  correct_answer: string
  passed: boolean
  explanation: string | null
}

export interface QuizResult {
  submission_id: number
  quiz_id: number
  user_id: string
  score: number
  max_score: number
  percentage: number
  passed: boolean
  results: QuestionResult[]
}

export interface UserProgress {
  user_id: string
  tier: 'free' | 'premium' | 'pro'
  completed_chapters: number[]
  quiz_scores: Record<string, number>
  current_streak: number
  longest_streak: number
  last_activity_date: string | null
  course_completion_pct: number
  total_quiz_score: number
}

export interface AccessCheck {
  access: boolean
  reason: string | null
  upgrade_url: string | null
}
