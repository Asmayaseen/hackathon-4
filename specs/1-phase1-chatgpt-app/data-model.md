# Data Model: Phase 1 ChatGPT App — Zero-Backend-LLM Course Companion

**Date**: 2026-03-09
**Branch**: `1-phase1-chatgpt-app`
**Database**: Neon (PostgreSQL 16)
**ORM**: SQLModel (Pydantic v2 + SQLAlchemy 2.0)

---

## Entity Relationship Overview

```
Chapter (1) ──────────── (0..1) Quiz
    │                              │
    │                              │ (1)
    │                    (many) QuizQuestion
    │                              │
    │                    (many) QuizSubmission ──── (1) User
    │
    │ (many)
ContentSection
    │
    └── (used by) Search

User (1) ──── (1) UserProgress
User (1) ──── (many) QuizSubmission
```

---

## Entity 1: Chapter

**Purpose**: Represents a single course content unit. Body text is stored in Cloudflare R2;
only metadata and a reference key are stored in Postgres.

```sql
CREATE TABLE chapters (
    id            SERIAL PRIMARY KEY,
    title         VARCHAR(255)    NOT NULL,
    r2_key        VARCHAR(512)    NOT NULL UNIQUE,  -- R2 object key for body text
    order_index   INTEGER         NOT NULL UNIQUE,  -- sequence position (1-based)
    tier          VARCHAR(10)     NOT NULL DEFAULT 'free'
                  CHECK (tier IN ('free', 'premium')),
    quiz_id       INTEGER         REFERENCES quizzes(id) ON DELETE SET NULL,
    summary       TEXT,                             -- 1-2 sentence preview (no LLM)
    created_at    TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);
```

**Rules**:
- `order_index` is unique and contiguous; gaps are not permitted.
- Chapters 1–3 MUST have `tier = 'free'`; Chapter 4+ MUST have `tier = 'premium'`.
- `r2_key` follows pattern: `chapters/{order_index}/{slug}.json`.
- `body` text is fetched from R2 at request time; never stored in Postgres.

**R2 Content Schema** (`chapters/{index}/{slug}.json`):
```json
{
  "chapter_id": 1,
  "title": "Introduction to AI Agents",
  "body": "<full markdown content>",
  "word_count": 1200
}
```

---

## Entity 2: ContentSection

**Purpose**: Pre-indexed searchable fragments of chapter content. Created at deploy time
by splitting chapter body into ~200-word sections. Powers the `/search` endpoint with
PostgreSQL full-text search.

```sql
CREATE TABLE content_sections (
    id            SERIAL PRIMARY KEY,
    chapter_id    INTEGER         NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    section_index INTEGER         NOT NULL,          -- position within chapter
    text          TEXT            NOT NULL,
    text_tsv      TSVECTOR        GENERATED ALWAYS AS (to_tsvector('english', text)) STORED,
    created_at    TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_content_sections_tsv ON content_sections USING GIN(text_tsv);
CREATE INDEX idx_content_sections_chapter ON content_sections(chapter_id);
```

**Rules**:
- Sections are ~150–250 words each (split on paragraph boundaries).
- `text_tsv` is auto-generated; never manually set.
- Populated by a seeding script at deploy time — not during API requests.

---

## Entity 3: Quiz

**Purpose**: Container for a chapter's multiple-choice quiz questions.

```sql
CREATE TABLE quizzes (
    id            SERIAL PRIMARY KEY,
    chapter_id    INTEGER         NOT NULL UNIQUE REFERENCES chapters(id) ON DELETE CASCADE,
    title         VARCHAR(255)    NOT NULL,
    created_at    TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);
```

---

## Entity 4: QuizQuestion

**Purpose**: Individual multiple-choice question. `correct_option` is NEVER returned
in API responses — only stored server-side for grading.

```sql
CREATE TABLE quiz_questions (
    id             SERIAL PRIMARY KEY,
    quiz_id        INTEGER         NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
    question_text  TEXT            NOT NULL,
    options        JSONB           NOT NULL,  -- {"A": "...", "B": "...", "C": "...", "D": "..."}
    correct_option VARCHAR(1)      NOT NULL   CHECK (correct_option IN ('A','B','C','D')),
    explanation    TEXT,                      -- shown after grading (not the answer)
    position       INTEGER         NOT NULL,  -- question order within quiz
    created_at     TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_quiz_questions_quiz ON quiz_questions(quiz_id);
```

**Rules**:
- Each quiz MUST have exactly 5 questions for Phase 1.
- `correct_option` is NEVER included in GET quiz endpoint responses.
- `explanation` is returned only in grading responses (POST submit).

---

## Entity 5: QuizSubmission

**Purpose**: Records a student's quiz attempt and computed grade.

```sql
CREATE TABLE quiz_submissions (
    id              SERIAL PRIMARY KEY,
    user_id         VARCHAR(128)    NOT NULL,
    quiz_id         INTEGER         NOT NULL REFERENCES quizzes(id),
    submitted_at    TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    answers         JSONB           NOT NULL,  -- {"question_id": "A", ...}
    score           INTEGER         NOT NULL,  -- number of correct answers
    max_score       INTEGER         NOT NULL,  -- total questions
    passed          BOOLEAN         NOT NULL   -- score >= 60% threshold
);

CREATE INDEX idx_submissions_user_quiz ON quiz_submissions(user_id, quiz_id);
```

**Rules**:
- Multiple submissions per user/quiz are allowed; each is stored independently.
- `passed` threshold: score / max_score >= 0.6 (60%).
- Progress record is updated to reflect the LATEST submission score.

---

## Entity 6: UserProgress

**Purpose**: Aggregated learning progress per student. Single record per user.

```sql
CREATE TABLE user_progress (
    user_id              VARCHAR(128)    PRIMARY KEY,
    tier                 VARCHAR(10)     NOT NULL DEFAULT 'free'
                         CHECK (tier IN ('free', 'premium', 'pro')),
    completed_chapters   INTEGER[]       NOT NULL DEFAULT '{}',  -- chapter IDs
    quiz_scores          JSONB           NOT NULL DEFAULT '{}',  -- {chapter_id: score}
    current_streak       INTEGER         NOT NULL DEFAULT 0,
    longest_streak       INTEGER         NOT NULL DEFAULT 0,
    last_activity_date   DATE,                                   -- UTC date
    created_at           TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);
```

**State transitions**:
- On chapter completion: `completed_chapters` appended, `last_activity_date` updated,
  streak recalculated.
- On quiz submission: `quiz_scores[chapter_id]` set to latest score.
- Streak logic: if `last_activity_date = TODAY - 1 day` → `streak + 1`;
  if `last_activity_date = TODAY` → no change;
  if `last_activity_date < TODAY - 1 day` → `streak = 1`.
- Auto-created with zero state on first write for unknown `user_id`.

**Computed fields** (not stored, calculated at query time):
- `course_completion_pct` = len(completed_chapters) / total_chapters × 100
- `total_quiz_score` = sum of all quiz_scores values

---

## Validation Rules Summary

| Entity | Rule | Error |
|--------|------|-------|
| Chapter | `tier` must be 'free' for chapters 1–3 | 400 Bad Request |
| ContentSection | text length 150–300 words | Seeding validation error |
| QuizQuestion | exactly 4 options (A/B/C/D) required | 400 Bad Request |
| QuizQuestion | `correct_option` in (A,B,C,D) | DB constraint |
| QuizSubmission | all question IDs must belong to the quiz | 400 Bad Request |
| QuizSubmission | all answers must be in (A,B,C,D) | 400 Bad Request |
| UserProgress | tier in (free, premium, pro) | DB constraint |
| UserProgress | streak cannot be negative | Application logic |

---

## Database Migrations Strategy

- Tool: **Alembic** (auto-generated from SQLModel definitions).
- Each schema change = one migration file; never edit existing migrations.
- Seeding (chapter content + quizzes) handled via separate `seed.py` script.
- `seed.py` runs after migration in CI/CD pipeline.
- R2 content upload handled by separate `upload_content.py` script.
