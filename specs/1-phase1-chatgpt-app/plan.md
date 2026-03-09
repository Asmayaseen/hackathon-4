# Implementation Plan: Phase 1 ChatGPT App — Zero-Backend-LLM Course Companion

**Branch**: `1-phase1-chatgpt-app` | **Date**: 2026-03-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-phase1-chatgpt-app/spec.md`

---

## Summary

Build a fully deterministic FastAPI backend (zero LLM inference) serving AI Agent Development
course content from Cloudflare R2, with PostgreSQL (Neon) for progress and quiz storage.
A ChatGPT App (OpenAI Agents SDK) acts as the sole intelligent layer, tutoring students using
content the backend serves verbatim. All 6 Phase 1 features must be implemented: content
delivery, navigation, grounded Q&A, rule-based quizzes, progress tracking, and freemium gate.

---

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI 0.110+, SQLModel, asyncpg, boto3 (R2), Alembic, Uvicorn
**Storage**: Neon (PostgreSQL 16) for progress/quiz data; Cloudflare R2 for chapter content
**Testing**: pytest + httpx (async test client) + pytest-asyncio
**Target Platform**: Linux server (Fly.io, Docker container)
**Project Type**: Web application (backend API + ChatGPT App frontend)
**Performance Goals**: p95 <500ms content delivery; <1s search; <500ms quiz grading
**Constraints**: Zero LLM API calls in backend (disqualification if violated); <$41/month
  infrastructure for 10k users; free tier must be limited to chapters 1–3
**Scale/Scope**: 10,000+ monthly active users; 1,000 concurrent users; 5+ chapters; 5 quizzes

---

## Constitution Check

*GATE: Must pass before implementation. Re-checked after Phase 1 design.*

| Principle | Gate | Status |
|-----------|------|--------|
| I. Zero-Backend-LLM | Backend source MUST have zero LLM imports or API calls | ✅ PASS — deterministic FastAPI only |
| II. Dual-Frontend | ChatGPT App is primary frontend (Phase 1); Web App deferred to Phase 3 | ✅ PASS — ChatGPT App built this phase |
| III. Phase-Gated | All 6 Phase 1 features implemented before Phase 2 begins | ✅ PASS — all 6 in scope |
| IV. Agent Skills | All 4 SKILL.md files created and embedded in ChatGPT App manifest | ✅ PASS — in scope |
| V. Cost Efficiency | R2 + Neon + Fly.io; <$41/mo for 10k users; freemium tiers implemented | ✅ PASS — stack confirmed in research |
| VI. Spec-Driven | spec.md ✅, plan.md ✅ (this file), tasks.md (next), OpenAPI ✅ | ✅ PASS |

**No violations found. No Complexity Tracking entries required.**

---

## Project Structure

### Documentation (this feature)

```text
specs/1-phase1-chatgpt-app/
├── plan.md              # This file
├── research.md          # Phase 0 — technology decisions
├── data-model.md        # Phase 1 — entity schemas
├── quickstart.md        # Phase 1 — end-to-end validation guide
├── contracts/
│   └── openapi.yaml     # Full OpenAPI 3.1 specification
├── checklists/
│   └── requirements.md  # Spec quality checklist (all pass)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── main.py                    # FastAPI app entry point, router registration
│   ├── config.py                  # Pydantic settings (env vars)
│   ├── database.py                # Async DB engine, session factory
│   ├── r2_client.py               # Cloudflare R2 boto3 client
│   ├── models/
│   │   ├── chapter.py             # Chapter, ChapterMeta SQLModel
│   │   ├── content_section.py     # ContentSection SQLModel + FTS index
│   │   ├── quiz.py                # Quiz, QuizQuestion SQLModel
│   │   ├── quiz_submission.py     # QuizSubmission SQLModel
│   │   └── user_progress.py       # UserProgress SQLModel
│   ├── schemas/
│   │   ├── chapter.py             # Pydantic response schemas
│   │   ├── search.py              # SearchResponse schema
│   │   ├── quiz.py                # QuizResponse, QuizResult schemas
│   │   ├── progress.py            # UserProgress response schema
│   │   └── access.py              # AccessCheck, AccessDenied schemas
│   ├── routers/
│   │   ├── chapters.py            # GET /chapters, /chapters/{id}, /next, /previous
│   │   ├── search.py              # GET /search
│   │   ├── quizzes.py             # GET /quizzes/chapter/{id}, POST /submit
│   │   ├── progress.py            # GET/PUT /progress/{user_id}
│   │   ├── access.py              # GET /access/check
│   │   └── health.py              # GET /health
│   └── services/
│       ├── content_service.py     # R2 fetch + chapter assembly
│       ├── search_service.py      # PostgreSQL FTS logic
│       ├── quiz_service.py        # Grading engine (rule-based)
│       ├── progress_service.py    # Streak calculation, progress updates
│       └── access_service.py      # Tier-based access control
├── migrations/
│   ├── env.py
│   └── versions/
│       ├── 001_create_schema.py
│       └── 002_create_user_progress.py
├── scripts/
│   ├── seed.py                    # Seed chapters, quizzes into DB + R2
│   └── upload_content.py          # Upload chapter JSON files to R2
├── tests/
│   ├── conftest.py                # Async test client, DB fixtures
│   ├── test_chapters.py           # Chapter delivery + navigation tests
│   ├── test_search.py             # Search/Q&A tests
│   ├── test_quizzes.py            # Quiz delivery + grading tests
│   ├── test_progress.py           # Progress tracking + streak tests
│   └── test_access.py             # Freemium gate tests
├── requirements.txt
├── Dockerfile
├── fly.toml
└── .env.example

chatgpt-app/
├── manifest.yaml                  # ChatGPT App YAML manifest (FR-011)
└── skills/
    ├── concept-explainer.md       # SKILL: explain concepts (FR-012)
    ├── quiz-master.md             # SKILL: guide quizzes (FR-012)
    ├── socratic-tutor.md          # SKILL: Socratic guidance (FR-012)
    └── progress-motivator.md      # SKILL: celebrate progress (FR-012)
```

**Structure Decision**: Web application layout (Option 2). Backend is a standalone FastAPI
service. ChatGPT App frontend is in a separate `chatgpt-app/` directory with its own
manifest and SKILL.md files. No shared source between frontend and backend.

---

## Architecture Decisions

### AD-1: Content Storage Split (R2 + PostgreSQL)

Chapter body text lives in Cloudflare R2 (zero egress cost). Only metadata and searchable
content sections live in PostgreSQL. The `content_service` fetches from R2 on each chapter
request, then returns verbatim — no caching in Phase 1 (acceptable for 1k concurrent users;
caching is a Phase 2 optimisation).

### AD-2: Full-Text Search via PostgreSQL tsvector

PostgreSQL GIN index on `content_sections.text_tsv` provides <100ms keyword search without
any additional infrastructure. Content sections are pre-indexed at deploy time by `seed.py`.
Query: `SELECT ... WHERE text_tsv @@ plainto_tsquery('english', :query) ORDER BY rank DESC`.

### AD-3: Stateless Request Handling

All requests are stateless — no server-side session state. User identity is the `X-User-ID`
header. All persistent state lives in PostgreSQL (progress, quiz submissions). This enables
horizontal scaling on Fly.io without sticky sessions.

### AD-4: Quiz Answer Key Never Leaves the Server

`GET /quizzes/chapter/{id}` returns `QuizQuestion` schema which excludes `correct_option`.
The answer key is only accessed inside `quiz_service.grade()`. The OpenAPI schema documents
this explicitly. Code review gate: `grep -r "correct_option" app/routers/` must return zero
matches.

### AD-5: ChatGPT App System Prompt Carries All Skills

All 4 SKILL.md files are concatenated into the ChatGPT App system prompt in `manifest.yaml`.
ChatGPT uses these as procedural knowledge for how to tutor. This satisfies FR-012 without
any backend changes.

---

## API Contract Summary

| Method | Endpoint | Feature | SLO |
|--------|----------|---------|-----|
| GET | `/chapters` | Content list | <300ms |
| GET | `/chapters/{id}` | Content delivery | <500ms (SC-001) |
| GET | `/chapters/{id}/next` | Navigation | <200ms |
| GET | `/chapters/{id}/previous` | Navigation | <200ms |
| GET | `/search` | Grounded Q&A | <1s (SC-002) |
| GET | `/quizzes/chapter/{id}` | Quiz delivery | <300ms |
| POST | `/quizzes/{id}/submit` | Rule-based grading | <500ms (SC-003) |
| GET | `/progress/{user_id}` | Progress tracking | <300ms (SC-004) |
| PUT | `/progress/{user_id}/chapters/{id}` | Progress update | <300ms |
| GET | `/access/check` | Freemium gate | <100ms |
| GET | `/health` | Health | <50ms |

Full schema: [`contracts/openapi.yaml`](./contracts/openapi.yaml)

---

## Non-Functional Requirements

### Performance
- p95 content delivery: <500ms (SC-001 relaxed to <2s worldwide, p95 target 500ms)
- p95 search: <1s (SC-002)
- p95 quiz grading: <500ms (SC-003)
- p95 progress read: <300ms (SC-004)

### Reliability
- 99.9% uptime via Fly.io auto-restart
- Graceful 503 when R2 is unreachable (edge case: content_unavailable)
- Zero-state auto-creation for unknown user IDs (no 404 on progress read)

### Security
- `X-User-ID` header is trusted (injected by ChatGPT platform)
- No user-controlled SQL input (parameterised queries via SQLModel)
- Answer key (`correct_option`) NEVER serialised in API responses
- No secrets in source code — all via `.env` / Fly.io secrets

### Cost (SC-007)
| Component | Monthly (10k users) |
|-----------|-------------------|
| Cloudflare R2 | ~$5 |
| Neon PostgreSQL | $0–$25 |
| Fly.io compute | ~$10 |
| Domain + SSL | ~$1 |
| **Total** | **$16–$41** |

---

## Risk Analysis

1. **R2 latency spikes** — Chapter body fetched from R2 per request. Mitigation: add
   in-memory LRU cache (10 chapters) in Phase 1.5 if p95 >500ms observed in testing.

2. **Neon cold starts** — Serverless PostgreSQL may have 100–200ms cold start.
   Mitigation: use connection pooling via pgBouncer (Neon built-in) and keep-alive pings.

3. **User ID spoofing** — No auth in Phase 1; any client can pass any `X-User-ID`.
   Mitigation: accepted risk for Phase 1; proper JWT auth added in Phase 2.

---

## Phase 0 Research Artifacts

All technology decisions documented in [`research.md`](./research.md):
- ✅ Python 3.11 + FastAPI 0.110 + Pydantic v2
- ✅ Neon (PostgreSQL 16) over Supabase
- ✅ Cloudflare R2 (JSON files) over AWS S3
- ✅ PostgreSQL FTS over Elasticsearch
- ✅ X-User-ID header (no JWT Phase 1)
- ✅ OpenAI Agents SDK for ChatGPT App
- ✅ Fly.io for deployment
- ✅ AI Agent Development course topic (Option A)

## Phase 1 Design Artifacts

- ✅ [`data-model.md`](./data-model.md) — 6 entities, full SQL schemas, validation rules
- ✅ [`contracts/openapi.yaml`](./contracts/openapi.yaml) — Complete OpenAPI 3.1 spec
- ✅ [`quickstart.md`](./quickstart.md) — 13-step end-to-end validation guide
