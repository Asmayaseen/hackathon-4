# Tasks: Phase 1 ChatGPT App — Zero-Backend-LLM Course Companion

**Input**: Design documents from `/specs/1-phase1-chatgpt-app/`
**Prerequisites**: plan.md ✅ | spec.md ✅ | data-model.md ✅ | contracts/openapi.yaml ✅ | research.md ✅

**Tests**: Test tasks included in Polish phase — run after all stories are complete.
**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1–US5)
- Exact file paths included in all descriptions

## Path Conventions

- Backend source: `backend/app/`
- Backend tests: `backend/tests/`
- ChatGPT App: `chatgpt-app/`
- Scripts: `backend/scripts/`
- Migrations: `backend/migrations/versions/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project skeleton, tooling, and deployment configuration

- [x] T001 Create backend/ directory tree: `app/{models,schemas,routers,services}`, `migrations/versions`, `scripts`, `tests` per plan.md structure
- [x] T002 Create `backend/requirements.txt` with pinned versions: fastapi==0.110.0, uvicorn[standard], sqlmodel, asyncpg, alembic, boto3, python-dotenv, httpx, pytest, pytest-asyncio
- [x] T003 [P] Create `backend/.env.example` with all required vars: DATABASE_URL, R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME
- [x] T004 [P] Create `backend/Dockerfile` using python:3.11-slim base with non-root user, pip install, uvicorn entrypoint
- [x] T005 [P] Create `fly.toml` with Fly.io app config: shared-cpu-1x, port 8000, health check `/health`, auto-stop disabled
- [x] T006 Create `chatgpt-app/` directory with `skills/` subdirectory

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Create `backend/app/config.py` with Pydantic `BaseSettings`: DATABASE_URL, R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME, APP_VERSION="1.0.0"
- [x] T008 Create `backend/app/database.py` with async SQLAlchemy engine (`create_async_engine`), `AsyncSession` factory, and `get_session` dependency
- [x] T009 Create `backend/app/r2_client.py` with boto3 S3 client pointed at Cloudflare R2 endpoint (`https://{account_id}.r2.cloudflarestorage.com`), `get_object()` and `put_object()` wrappers
- [x] T010 Create `backend/app/main.py` with FastAPI app instance, lifespan context (DB connect/disconnect), CORS middleware (allow all origins Phase 1), and router registration stubs
- [x] T011 Create `backend/migrations/env.py` with async Alembic config using `asyncpg`, targeting all SQLModel metadata
- [x] T012 Create `backend/migrations/versions/001_create_chapters_quizzes_sections.py` — tables: `chapters`, `quizzes`, `quiz_questions`, `content_sections` with GIN tsvector index per data-model.md
- [x] T013 Create `backend/migrations/versions/002_create_progress_submissions.py` — tables: `user_progress`, `quiz_submissions` per data-model.md

**Checkpoint**: Foundation ready — `alembic upgrade head` must succeed before user story work begins

---

## Phase 3: User Story 1 — Content Delivery & Chapter Navigation (Priority: P1) 🎯 MVP

**Goal**: Students can fetch any chapter's full content and navigate next/previous chapters

**Independent Test**: Run `GET /chapters/1` → returns body text from R2. Run `GET /chapters/1/next` → returns chapter 2 metadata. Run `GET /chapters/1/previous` → returns boundary indicator. No LLM calls made.

### Implementation for User Story 1

- [x] T014 [P] [US1] Create `backend/app/models/chapter.py` with `Chapter` SQLModel: id, title, r2_key, order_index, tier (free/premium), quiz_id (nullable FK), summary, created_at
- [x] T015 [P] [US1] Create `backend/app/models/content_section.py` with `ContentSection` SQLModel: id, chapter_id (FK), section_index, text, text_tsv (GENERATED tsvector), created_at
- [x] T016 [P] [US1] Create `backend/app/schemas/chapter.py` with Pydantic schemas: `ChapterMeta`, `Chapter` (extends ChapterMeta + body + word_count), `ChapterNavigation` — matching `contracts/openapi.yaml`
- [x] T017 [US1] Create `backend/app/services/content_service.py` with `get_chapter(chapter_id, session)` → fetches metadata from DB + body from R2 using r2_client; `get_chapter_meta_list(session)` → returns all chapters metadata
- [x] T018 [US1] Create `backend/app/routers/chapters.py` with 4 endpoints: `GET /chapters`, `GET /chapters/{chapter_id}`, `GET /chapters/{chapter_id}/next`, `GET /chapters/{chapter_id}/previous` — all require `X-User-ID` header
- [x] T019 [US1] Register chapters router in `backend/app/main.py` with prefix `/chapters`
- [x] T020 [P] [US1] Create `backend/app/routers/health.py` with `GET /health` returning `{"status": "ok", "version": settings.APP_VERSION}`
- [x] T021 [US1] Register health router in `backend/app/main.py`
- [x] T022 [P] [US1] Create `backend/scripts/upload_content.py` — reads JSON files from `content/chapters/*.json`, uploads each to R2 at key `chapters/{order_index}/{slug}.json`
- [x] T023 [US1] Create `backend/scripts/seed.py` — inserts chapter records into DB, splits body text into 150–250 word sections, inserts ContentSection records; also seeds 5 chapters of AI Agent Development content (titles + placeholder body text)

**Checkpoint**: `GET /chapters/1` returns full chapter; `/next` and `/previous` work; health check passes ✅

---

## Phase 4: User Story 2 — Grounded Q&A (Priority: P2)

**Goal**: Students can search course content and get grounded answers via ChatGPT

**Independent Test**: Run `GET /search?q=What+is+MCP` with `X-User-ID` header → returns 3–5 sections with `chapter_id` and `text`. Run with nonsense query → returns `{"no_results": true, "sections": []}`.

### Implementation for User Story 2

- [x] T024 [P] [US2] Create `backend/app/schemas/search.py` with `SearchResponse` and `ContentSection` schemas matching `contracts/openapi.yaml`
- [x] T025 [US2] Create `backend/app/services/search_service.py` with `search_content(query, user_id, limit, session)` — executes `SELECT ... WHERE text_tsv @@ plainto_tsquery('english', :query) ORDER BY ts_rank(text_tsv, query) DESC LIMIT :limit`; filters results to chapters accessible by user tier
- [x] T026 [US2] Create `backend/app/routers/search.py` with `GET /search` endpoint: validates `q` param (2–500 chars), calls search_service, returns SearchResponse
- [x] T027 [US2] Register search router in `backend/app/main.py` with prefix `/search` (or no prefix, path is `/search`)

**Checkpoint**: Search returns ranked results from content_sections; no-results case handled; free-tier search filtered to chapters 1–3 ✅

---

## Phase 5: User Story 3 — Rule-Based Quizzes (Priority: P2)

**Goal**: Students can take chapter quizzes and receive deterministic graded results

**Independent Test**: Run `GET /quizzes/chapter/1` → returns 5 questions WITHOUT `correct_option` field. Run `POST /quizzes/1/submit` with all answers → returns score, per-question pass/fail, and correct answers. Run `grep -r "correct_option" backend/app/routers/` → zero matches.

### Implementation for User Story 3

- [x] T028 [P] [US3] Create `backend/app/models/quiz.py` with `Quiz` SQLModel (id, chapter_id FK, title) and `QuizQuestion` SQLModel (id, quiz_id FK, question_text, options JSONB, correct_option, explanation, position)
- [x] T029 [P] [US3] Create `backend/app/models/quiz_submission.py` with `QuizSubmission` SQLModel: id, user_id, quiz_id FK, submitted_at, answers JSONB, score, max_score, passed
- [x] T030 [P] [US3] Create `backend/app/schemas/quiz.py` with `QuizQuestion` (NO correct_option), `QuizResponse`, `QuizSubmissionRequest`, `QuizResult`, `QuestionResult` schemas matching `contracts/openapi.yaml`
- [x] T031 [US3] Create `backend/app/services/quiz_service.py` with `get_quiz_by_chapter(chapter_id, session)` and `grade_submission(quiz_id, user_id, answers, session)` — compares answers to stored `correct_option`, computes score, sets passed=score/max>=0.6, saves QuizSubmission record
- [x] T032 [US3] Create `backend/app/routers/quizzes.py` with `GET /quizzes/chapter/{chapter_id}` and `POST /quizzes/{quiz_id}/submit` — validate all question IDs present, return 400 for incomplete submissions
- [x] T033 [US3] Register quizzes router in `backend/app/main.py`
- [x] T034 [US3] Extend `backend/scripts/seed.py` to seed 5 quizzes (one per chapter) with 5 questions each, including `correct_option` and `explanation` for AI Agent Development content

**Checkpoint**: Quiz questions returned without answer key; grading returns accurate scores; QuizSubmission saved to DB ✅

---

## Phase 6: User Story 4 — Progress Tracking & Streaks (Priority: P3)

**Goal**: Student completion and daily streaks are persisted and retrievable

**Independent Test**: Run `PUT /progress/test_user/chapters/1` → progress record created with `completed_chapters: [1]`, `current_streak: 1`. Run `GET /progress/test_user` → returns full summary. Run `GET /progress/unknown_user` → returns zero-state (not 404).

### Implementation for User Story 4

- [x] T035 [P] [US4] Create `backend/app/models/user_progress.py` with `UserProgress` SQLModel: user_id (PK), tier, completed_chapters (ARRAY), quiz_scores (JSONB), current_streak, longest_streak, last_activity_date, created_at, updated_at
- [x] T036 [P] [US4] Create `backend/app/schemas/progress.py` with `UserProgress` response schema (+ computed fields: course_completion_pct, total_quiz_score) matching `contracts/openapi.yaml`
- [x] T037 [US4] Create `backend/app/services/progress_service.py` with: `get_or_create_progress(user_id, session)` (auto-creates zero-state), `mark_chapter_complete(user_id, chapter_id, session)` (appends to array, recalculates streak), `update_quiz_score(user_id, chapter_id, score, session)` with streak logic: today==last_date→no change; today==last_date+1→streak+1; else→streak=1
- [x] T038 [US4] Create `backend/app/routers/progress.py` with `GET /progress/{user_id}` and `PUT /progress/{user_id}/chapters/{chapter_id}`
- [x] T039 [US4] Register progress router in `backend/app/main.py`
- [x] T040 [US4] Call `progress_service.update_quiz_score()` from `quiz_service.grade_submission()` after saving submission to keep progress in sync

**Checkpoint**: Chapter completion persists across requests; streak increments on consecutive days; unknown users auto-created ✅

---

## Phase 7: User Story 5 — Freemium Access Gate (Priority: P3)

**Goal**: Free-tier students blocked from premium content; premium students have full access

**Independent Test**: `GET /access/check?user_id=free_user&resource=chapter_4` → `{"access": false, "reason": "premium_required"}`. `GET /chapters/4` with free-user header → 403 AccessDenied. `GET /chapters/1` with free-user header → 200 full content.

### Implementation for User Story 5

- [x] T041 [P] [US5] Create `backend/app/schemas/access.py` with `AccessCheck` and `AccessDenied` schemas matching `contracts/openapi.yaml`
- [x] T042 [US5] Create `backend/app/services/access_service.py` with `check_access(user_id, resource, session)` — fetches user tier from UserProgress (default free), applies rule: free tier → chapters 1–3 only; premium/pro → all chapters; returns `AccessCheck` model
- [x] T043 [US5] Create `backend/app/routers/access.py` with `GET /access/check` endpoint
- [x] T044 [US5] Register access router in `backend/app/main.py`
- [x] T045 [US5] Enforce access control in `backend/app/routers/chapters.py` — call `access_service.check_access()` before fetching chapter; return 403 `AccessDenied` if access=False
- [x] T046 [US5] Enforce access control in `backend/app/routers/quizzes.py` — same pattern as T045 for quiz endpoints
- [x] T047 [US5] Update `backend/app/services/search_service.py` to filter content_sections by user-accessible chapter IDs (get accessible chapters from access_service, add WHERE clause)

**Checkpoint**: Free user blocked at chapter 4+; premium user passes; chapters 1–3 always accessible; search filtered by tier ✅

---

## Phase 8: ChatGPT App & Agent Skills

**Goal**: ChatGPT App manifest and all 4 SKILL.md files created and integrated

**Independent Test**: `manifest.yaml` validates against OpenAI Agents SDK schema. Each SKILL.md contains: Metadata, Purpose, Workflow, Response Templates, Key Principles sections.

### Implementation for ChatGPT App

- [x] T048 [P] Create `chatgpt-app/skills/concept-explainer.md` — Metadata (name: concept-explainer, triggers: "explain", "what is", "how does"), Purpose, Workflow (fetch content → simplify → give analogy → check understanding), Response Templates, Principles (only use provided content, never hallucinate)
- [x] T049 [P] Create `chatgpt-app/skills/quiz-master.md` — Metadata (triggers: "quiz", "test me", "practice"), Workflow (call GET /quizzes/chapter/{id} → present one question at a time → collect answer → submit batch → explain wrong answers using content), Response Templates (encouragement, score celebration)
- [x] T050 [P] Create `chatgpt-app/skills/socratic-tutor.md` — Metadata (triggers: "help me think", "I'm stuck"), Workflow (ask guiding question → wait for response → give hint → never give direct answer → lead to insight), Response Templates
- [x] T051 [P] Create `chatgpt-app/skills/progress-motivator.md` — Metadata (triggers: "my progress", "streak", "how am I doing"), Workflow (call GET /progress/{user_id} → format results → celebrate milestones → suggest next chapter), Response Templates (streak celebrations, encouragement)
- [x] T052 Create `chatgpt-app/manifest.yaml` — OpenAI Agents SDK YAML manifest with: `name`, `description`, `system_prompt` (embeds all 4 SKILL.md contents), `actions` (one per API endpoint from openapi.yaml: listChapters, getChapter, getNextChapter, getPreviousChapter, searchContent, getQuizByChapter, submitQuiz, getUserProgress, markChapterComplete, checkAccess), `api.url` pointing to backend

**Checkpoint**: manifest.yaml references all 10 API actions; system_prompt contains all 4 skill procedures; triggers mapped correctly ✅

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Tests, docs, and final validation across all user stories

- [x] T053 [P] Create `backend/tests/test_chapters.py` — test GET /chapters/1 returns body; GET /chapters/1/next returns chapter 2; GET /chapters/1/previous returns boundary; GET /chapters/99 returns 404
- [x] T054 [P] Create `backend/tests/test_search.py` — test known query returns relevant sections; unknown query returns no_results=true; free-user search excludes premium chapter sections
- [x] T055 [P] Create `backend/tests/test_quizzes.py` — test GET /quizzes/chapter/1 has no correct_option field; POST /submit with correct answers scores 5/5; incomplete submission returns 400
- [x] T056 [P] Create `backend/tests/test_progress.py` — test chapter completion persists; streak increments; unknown user auto-created; missed day resets streak
- [x] T057 [P] Create `backend/tests/test_access.py` — test free user blocked at chapter 4; premium user passes; chapters 1–3 always pass; /access/check endpoint returns correct schema
- [x] T058 Verify Zero-LLM compliance: run `grep -r "anthropic\|openai\|langchain\|litellm\|ollama" backend/app/ --include="*.py"` — MUST return zero matches; document result in `docs/zero-llm-audit.md`
- [x] T059 [P] Create `README.md` with: project overview, local setup steps, environment variables reference, architecture diagram placeholder, cost analysis summary, links to spec/plan/openapi
- [x] T060 [P] Create `docs/cost-analysis.md` with Phase 1 cost breakdown table: R2 ($5), Neon ($0–$25), Fly.io ($10), Domain ($1), total $16–$41 per 10k users, $0.002–$0.004 per user/month

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Phase 2 — first story, no other story deps
- **US2 (Phase 4)**: Depends on Phase 2 + ContentSection model from US1 (T015)
- **US3 (Phase 5)**: Depends on Phase 2 — independent of US1/US2
- **US4 (Phase 6)**: Depends on Phase 2 — independent, but T040 integrates with US3
- **US5 (Phase 7)**: Depends on Phase 2 + UserProgress from US4 (T035) + Chapter model from US1 (T014)
- **ChatGPT App (Phase 8)**: Depends on all backend endpoints (Phases 3–7)
- **Polish (Phase 9)**: Depends on all implementation phases complete

### User Story Cross-Dependencies

| Story | Depends On | Integration Point |
|-------|-----------|-------------------|
| US1 (Content) | Phase 2 only | ContentSection model reused by US2 |
| US2 (Search) | Phase 2 + US1 T015 | Queries content_sections table |
| US3 (Quizzes) | Phase 2 only | T040 calls progress_service (US4) |
| US4 (Progress) | Phase 2 only | UserProgress.tier used by US5 access_service |
| US5 (Access) | Phase 2 + US1 T014 + US4 T035 | access_service reads UserProgress |

### Within Each User Story

- Models ([P]) before services
- Services before routers
- Router registration in main.py after router creation
- Seed data required before end-to-end testing

---

## Parallel Execution Examples

### User Story 1 (P1) — Can parallelize models + schemas

```bash
# Run in parallel:
Task T014: Create backend/app/models/chapter.py
Task T015: Create backend/app/models/content_section.py
Task T016: Create backend/app/schemas/chapter.py
Task T020: Create backend/app/routers/health.py
Task T022: Create backend/scripts/upload_content.py
# Then sequentially:
Task T017: Create content_service.py (needs T014, T015)
Task T018: Create chapters router (needs T017)
```

### User Story 3 (P2) — Can parallelize models

```bash
# Run in parallel:
Task T028: Create backend/app/models/quiz.py
Task T029: Create backend/app/models/quiz_submission.py
Task T030: Create backend/app/schemas/quiz.py
# Then sequentially:
Task T031: Create quiz_service.py (needs T028, T029, T030)
Task T032: Create quizzes router (needs T031)
```

### ChatGPT App Skills (Phase 8) — All 4 skills in parallel

```bash
# Run in parallel:
Task T048: Create concept-explainer.md
Task T049: Create quiz-master.md
Task T050: Create socratic-tutor.md
Task T051: Create progress-motivator.md
# Then:
Task T052: Create manifest.yaml (needs T048–T051)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks everything)
3. Complete Phase 3: US1 (Content Delivery + Navigation)
4. **STOP and VALIDATE**: Run quickstart.md Steps 1–6
5. Deploy to Fly.io and test ChatGPT App manifest with US1 actions only

### Incremental Delivery

1. Setup + Foundational → DB and R2 connected
2. US1 complete → students can read chapters and navigate (MVP!)
3. US2 complete → students can ask grounded questions
4. US3 complete → students can take quizzes
5. US4 complete → progress and streaks tracked
6. US5 complete → freemium gate enforced
7. ChatGPT App → full tutoring experience in ChatGPT
8. Polish → tests, docs, Zero-LLM audit ✅

### Parallel Team Strategy (2 developers)

- **Developer A**: US1 (content) → US2 (search) → US5 (access)
- **Developer B**: US3 (quizzes) → US4 (progress) → ChatGPT App
- Both: Setup + Foundational together first; Polish together last

---

## Notes

- **[P]** = different files, no unresolved dependencies — safe to parallelise
- **[USn]** = maps task to specific user story for traceability
- Test tasks in Phase 9 are independent of each other — all can run in parallel
- Seed data (T023, T034) must be run before any endpoint testing
- T058 (Zero-LLM audit) is a HARD GATE — fail = disqualification risk
- Each story checkpoint must pass before starting Phase 8 (ChatGPT App)
- Total tasks: **60** across 9 phases
