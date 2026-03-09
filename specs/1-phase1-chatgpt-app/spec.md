# Feature Specification: Phase 1 ChatGPT App — Zero-Backend-LLM Course Companion

**Feature Branch**: `1-phase1-chatgpt-app`
**Created**: 2026-03-09
**Status**: Draft
**Input**: Phase 1 ChatGPT App — Zero Backend LLM with all 6 required features: content delivery,
navigation, grounded Q&A, rule-based quizzes, progress tracking, and freemium gate using
FastAPI and Cloudflare R2

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Content Delivery & Chapter Navigation (Priority: P1)

A student opens the Course Companion inside ChatGPT and asks to start learning. The ChatGPT
App calls the backend to fetch the first available chapter content. The backend returns the
raw chapter text verbatim from Cloudflare R2. ChatGPT then explains, summarises, and tutors
the student using that content. The student can move to the next or previous chapter at any
time.

**Why this priority**: Content delivery is the foundation of the entire product. Without it,
no other feature has meaning. It is also the primary value proposition — 24/7 course access.

**Independent Test**: A student can fetch Chapter 1, read it via ChatGPT, and navigate to
Chapter 2 using only this feature. The entire learning flow for a single chapter is complete.

**Acceptance Scenarios**:

1. **Given** a student requests Chapter 1, **When** the backend receives `GET /chapters/1`,
   **Then** the response returns the full chapter text, title, and metadata within 500ms.
2. **Given** a student is on Chapter 2, **When** they request the next chapter,
   **Then** `GET /chapters/2/next` returns Chapter 3 details (or an end-of-course indicator
   if no next chapter exists).
3. **Given** a student is on Chapter 1, **When** they request the previous chapter,
   **Then** `GET /chapters/1/previous` returns a boundary indicator (no previous chapter).
4. **Given** a student requests a non-existent chapter ID, **When** the backend processes
   the request, **Then** a 404 response with a clear error message is returned.

---

### User Story 2 — Grounded Q&A (Priority: P2)

A student asks a question about course content. The ChatGPT App calls the backend search
endpoint with the student's query. The backend returns the most relevant content sections
(keyword or semantic search against R2 content). ChatGPT answers the question using ONLY
those returned sections — never hallucinating outside the content.

**Why this priority**: Grounded Q&A is the core tutoring interaction. It ensures accuracy
and prevents hallucination, which is critical for educational trust.

**Independent Test**: A student can ask "What is an MCP server?" and receive an answer
grounded exclusively in the returned content sections. Testable by submitting a known
query and verifying the returned sections contain the answer.

**Acceptance Scenarios**:

1. **Given** a student asks a question, **When** `GET /search?q=<query>` is called,
   **Then** the backend returns the top 3–5 most relevant content sections with their
   chapter references within 800ms.
2. **Given** the search query matches no content, **When** the backend processes the request,
   **Then** an empty results array is returned with a `no_results` indicator so ChatGPT
   can tell the student the topic is not covered.
3. **Given** the search returns results, **When** ChatGPT responds, **Then** ChatGPT MUST
   only answer from the returned sections (enforced via system prompt in the ChatGPT App
   manifest).

---

### User Story 3 — Rule-Based Quizzes (Priority: P2)

A student asks to be tested on a chapter. The ChatGPT App retrieves quiz questions from the
backend for that chapter. The student answers through ChatGPT. ChatGPT presents results by
submitting answers to the backend, which grades them using a pre-defined answer key (no LLM
involved). ChatGPT then encourages and explains wrong answers using the content.

**Why this priority**: Quizzes provide measurable learning validation. Rule-based grading
ensures zero-cost, deterministic, auditable assessment.

**Independent Test**: A student takes a 5-question quiz for Chapter 1. Correct answers receive
a pass, wrong answers receive a fail — all determined by the backend answer key without any
LLM call.

**Acceptance Scenarios**:

1. **Given** a student requests a quiz for Chapter 1, **When** `GET /quizzes/chapter/1` is
   called, **Then** the backend returns a list of multiple-choice questions with answer options
   (answer key NOT included in the response).
2. **Given** a student submits quiz answers, **When** `POST /quizzes/{quiz_id}/submit` is
   called with answer selections, **Then** the backend returns a score, per-question
   pass/fail, and correct answers — all computed from the stored answer key.
3. **Given** a student submits an incomplete quiz (missing answers), **When** the backend
   processes the submission, **Then** a 400 error is returned indicating which questions
   are unanswered.

---

### User Story 4 — Progress Tracking & Streaks (Priority: P3)

The system tracks each student's chapter completion, quiz scores, and daily learning streaks.
When a student completes a chapter or quiz, the backend records this. Students can ask
ChatGPT "How am I doing?" and ChatGPT calls the backend to retrieve their progress summary.
ChatGPT then motivates and celebrates achievements.

**Why this priority**: Progress tracking creates engagement and accountability. It enables
the `progress-motivator` skill and supports the freemium gate (tracking what's been accessed).

**Independent Test**: A student completes Chapter 1 and takes its quiz. Their progress record
shows 1 chapter completed, quiz score recorded, streak incremented. Retrievable via
`GET /progress/{user_id}`.

**Acceptance Scenarios**:

1. **Given** a student completes a chapter, **When** `PUT /progress/{user_id}/chapters/{id}`
   is called with a completion status, **Then** the backend stores the completion with a
   timestamp and returns the updated progress summary.
2. **Given** a student completes a quiz, **When** progress is updated with a quiz score,
   **Then** the backend stores the score, updates the streak if the student has learned
   on consecutive days, and returns the updated summary.
3. **Given** a student requests their progress, **When** `GET /progress/{user_id}` is called,
   **Then** the backend returns completed chapters count, total quiz scores, current streak
   (days), and percentage of course completed.
4. **Given** a student misses a day, **When** progress is retrieved the next day,
   **Then** the streak counter is reset to 0.

---

### User Story 5 — Freemium Access Gate (Priority: P3)

Free-tier students can access the first 3 chapters and their associated quizzes. Attempting
to access Chapter 4 or beyond returns a `premium_required` response. Premium students can
access all chapters. The ChatGPT App checks access before fetching content so ChatGPT can
gracefully explain the upgrade path.

**Why this priority**: The freemium gate is required for monetisation viability and is
explicitly listed in the hackathon judging rubric.

**Independent Test**: A free-tier user ID attempting to access Chapter 4 receives a
`403 premium_required` response. A premium user ID accessing Chapter 4 receives full content.

**Acceptance Scenarios**:

1. **Given** a free-tier student requests Chapter 4, **When** `GET /access/check?user_id=X&resource=chapter_4` is called, **Then** the backend returns `{"access": false, "reason": "premium_required", "upgrade_url": "..."}`.
2. **Given** a premium student requests Chapter 4, **When** the access check is called,
   **Then** the backend returns `{"access": true}` and the content endpoint returns the
   full chapter.
3. **Given** any student requests Chapters 1–3, **When** the access check is called,
   **Then** the backend returns `{"access": true}` regardless of their tier.

---

### Edge Cases

- What happens when a chapter has no associated quiz? — Return empty quiz list with
  `no_quiz_available` indicator; ChatGPT skips quiz prompt for that chapter.
- What happens when a user ID is unrecognised? — A new progress record is auto-created
  on first write; reads return a zero-state progress object (not a 404).
- What happens when Cloudflare R2 is unreachable? — Backend returns 503 with a
  `content_unavailable` message; ChatGPT informs the student to try again shortly.
- What happens when a student submits answers for an already-completed quiz? —
  Re-submission is allowed; the new score overwrites the old one and progress is updated.
- What happens when search returns content from premium chapters for a free user? —
  Search results are filtered to only return sections from chapters the user has access to.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Backend MUST serve chapter content verbatim from Cloudflare R2 storage with
  no transformation, summarisation, or LLM processing.
- **FR-002**: Backend MUST provide sequential navigation — next and previous chapter
  endpoints — with boundary handling at first and last chapters.
- **FR-003**: Backend MUST provide keyword or semantic search across course content,
  returning the top relevant sections with chapter references.
- **FR-004**: Backend MUST store and serve pre-authored multiple-choice quiz questions
  with a hidden server-side answer key.
- **FR-005**: Backend MUST grade quiz submissions deterministically using the stored
  answer key and return per-question results and total score.
- **FR-006**: Backend MUST persist student progress including chapter completions,
  quiz scores, and daily streak counts per user ID.
- **FR-007**: Backend MUST enforce access control: free tier (Chapters 1–3 only),
  premium tier (all chapters), returning structured access-denied responses.
- **FR-008**: Backend MUST return structured JSON responses compatible with the OpenAI
  Agents SDK (ChatGPT App) for all endpoints.
- **FR-009**: Backend MUST expose a complete OpenAPI/Swagger documentation for all endpoints.
- **FR-010**: Backend MUST contain ZERO LLM API calls, RAG pipelines, prompt orchestration,
  or agent loops (Phase 1 strict constraint).
- **FR-011**: The ChatGPT App MUST include a valid YAML App Manifest defining all available
  actions, system prompt, and skill trigger keywords.
- **FR-012**: The system MUST include all 4 SKILL.md files: `concept-explainer`,
  `quiz-master`, `socratic-tutor`, `progress-motivator`.

### Key Entities

- **Chapter**: Course content unit with ID, title, body text (from R2), order index,
  access tier (free/premium), and associated quiz ID.
- **Quiz**: Set of multiple-choice questions for a chapter, with server-side answer key,
  question text, and answer options.
- **QuizSubmission**: Student's answers for a quiz, graded result (score, per-question
  pass/fail), and timestamp.
- **UserProgress**: Per-student record of completed chapter IDs, quiz scores by chapter,
  current streak (days), last activity date, and access tier.
- **ContentSection**: Indexed searchable fragment of chapter content, used for Q&A grounding.
- **AccessPolicy**: Rules mapping user tier (free/premium) to allowed chapter IDs.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A student can access and read any free-tier chapter within 2 seconds of
  requesting it, from anywhere in the world.
- **SC-002**: Search results for a student question are returned within 1 second and contain
  at least one relevant content section for any question that has a covered answer.
- **SC-003**: Quiz grading returns a complete result within 500ms of submission with 100%
  accuracy against the answer key.
- **SC-004**: Progress data is persisted durably — a student's completion state and streak
  survive a backend restart and are retrievable within 300ms.
- **SC-005**: Freemium gate blocks 100% of free-tier requests to premium content, with zero
  false positives for free-tier content.
- **SC-006**: The system supports at minimum 1,000 concurrent students with no degradation
  in response times above the thresholds defined in SC-001 through SC-004.
- **SC-007**: Total backend infrastructure cost for 10,000 monthly active users MUST remain
  below $41/month (Cloudflare R2 + DB + compute).
- **SC-008**: Zero LLM API calls originate from the backend during any Phase 1 operation —
  verified by code review and API call audit.
- **SC-009**: All 6 required features pass functional testing within the ChatGPT App
  interface without requiring any backend LLM inference.
- **SC-010**: A first-time student can begin learning (fetch Chapter 1, ask a question,
  and take a quiz) within 3 minutes of first interaction with the ChatGPT App.

### Assumptions

- Student identity is provided by the ChatGPT App as a user ID in request headers or
  query parameters; no separate authentication flow is required in Phase 1.
- Course content (chapter text, quiz questions, answer keys) is pre-authored and uploaded
  to Cloudflare R2 before the system goes live; content creation is out of scope.
- The selected course topic is **AI Agent Development** (Claude Agent SDK concepts, MCP,
  Agent Skills) as per Option A in the hackathon document.
- Semantic search (embeddings) is a stretch goal; keyword search is the minimum viable
  implementation for Phase 1.
- Daily streak is determined by UTC date of last activity; timezone handling is not
  required in Phase 1.
