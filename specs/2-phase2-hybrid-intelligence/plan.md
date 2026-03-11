# Architecture Plan: Phase 2 — Hybrid Intelligence (Premium)

**Feature**: Phase 2 Hybrid Intelligence
**Branch**: `2-phase2-hybrid-intelligence`
**Created**: 2026-03-10
**Status**: Implemented
**Builds On**: Phase 1 (`specs/1-phase1-chatgpt-app/plan.md`)

---

## Constitution Check ✅

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Zero-Backend-LLM (Phase 1) | ✅ | Phase 1 routes remain 100% zero-LLM |
| II. Dual-Frontend Architecture | ✅ | Web frontend has `/synthesis` page; ChatGPT app unchanged |
| III. Phase-Gated Feature Delivery | ✅ | Phase 2 only adds `/hybrid/*` routes; Phase 1 untouched |
| IV. Agent Skills | ✅ | No new skills required for Phase 2 backend features |
| V. Cost Efficiency | ✅ | `hybrid_usage` table tracks every token/cost; Pro gate prevents free tier abuse |
| VI. Spec-Driven Development | ✅ | spec.md → plan.md → tasks.md → implementation |

---

## Scope

### In Scope
- `POST /hybrid/assess` — LLM-graded free-form written answer assessment
- `POST /hybrid/synthesize` — Cross-chapter concept synthesis
- `GET /hybrid/usage/{user_id}` — Per-user cost tracking
- `HybridUsage` DB table for cost logging
- Frontend: Assessment tab on chapter pages + `/synthesis` page
- Mock mode when `ANTHROPIC_API_KEY` is not set

### Out of Scope
- Adaptive Learning Path (not chosen — would require user history ML)
- AI Mentor Agent (not chosen — requires multi-turn agent loop, Phase 3)
- Any changes to Phase 1 routes
- ChatGPT App changes (Phase 1 manifest unchanged)

---

## Key Decisions & Rationale

### Decision 1: Choose Features B (LLM Assessment) + C (Cross-Chapter Synthesis)

**Options considered:**
- A. Adaptive Learning Path — requires persistent learning model, high complexity
- B. LLM-Graded Assessments — clear value, bounded cost, user-initiated
- C. Cross-Chapter Synthesis — clear value, multi-document reasoning impossible without LLM
- D. AI Mentor Agent — too broad for Phase 2, better in Phase 3

**Rationale:** B and C have the clearest "why LLM is necessary" justification — both are impossible with deterministic rule-based logic. They are user-initiated and cost-predictable.

### Decision 2: Mock Mode by Default

**Rationale:** Enables demo without API key. Mock returns realistic responses with `[DEMO MODE]` label. Real Claude calls activate only when valid `ANTHROPIC_API_KEY` is present. This removes setup friction for judges/reviewers.

### Decision 3: Isolation via `/hybrid/*` route prefix

**Rationale:** Clean separation from Phase 1 routes. A grep for "anthropic" in the codebase returns only `hybrid_service.py` — making Phase 1 compliance trivially auditable.

### Decision 4: Pro tier gate (not Premium)

**Rationale:** LLM calls cost $0.014–0.027/request. Premium ($9.99/mo) tier is not priced to absorb unlimited LLM usage. Pro ($19.99/mo) is the correct monetisation level for these features.

---

## API Contracts

### POST /hybrid/assess
```
Headers: X-User-ID: <string>
Body:    { chapter_id: int, question: string, student_answer: string (max 1000 chars) }
200:     { score: 0-10, feedback: string, strengths: [], improvements: [], tokens_used: int, cost_usd: decimal }
400:     { detail: "student_answer is required" }
403:     { error: "pro_required", message: "...", upgrade_url: "...", your_tier: "free|premium" }
500:     { detail: "Assessment failed: <error>" }
```

### POST /hybrid/synthesize
```
Headers: X-User-ID: <string>
Body:    { chapter_ids: [int] (2–5), focus_question?: string }
200:     { synthesis: markdown, chapters_used: [string], tokens_used: int, cost_usd: decimal }
400:     { detail: "chapter_ids must contain 2–5 chapters" }
403:     { error: "pro_required", ... }
404:     { detail: "chapter X not found" }
500:     { detail: "Synthesis failed: <error>" }
```

### GET /hybrid/usage/{user_id}
```
Headers: X-User-ID: <string> (must match user_id)
200:     { user_id, total_requests, total_cost_usd, records: [...] }
403:     "Cannot view another user's usage."
```

---

## Data Model

### HybridUsage (new table)
```python
user_id:       str        # FK reference (not enforced — user may not have progress row)
feature:       str        # "assess" | "synthesize"
chapter_ids:   str        # JSON array, e.g. "[1,2,3]"
tokens_input:  int
tokens_output: int
cost_usd:      float
created_at:    datetime   # auto-set by DB
```

---

## Non-Functional Requirements

| Requirement | Target | Implementation |
|-------------|--------|----------------|
| Latency (assess) | p95 < 10s | Claude Sonnet max_tokens=500 |
| Latency (synthesize) | p95 < 15s | Claude Sonnet max_tokens=800 |
| Cost per assess | ≤ $0.020 | ~1,500 tokens at $3/$15 per M |
| Cost per synthesize | ≤ $0.030 | ~2,500 tokens at $3/$15 per M |
| Phase 1 impact | Zero | Separate router, service, model |
| Free/Premium gate | 100% enforced | `_require_pro()` on every endpoint |

---

## Architecture Pattern

```
ChatGPT App / Web Frontend
        ↓
FastAPI Backend
  ├─ Phase 1 Routes (deterministic — ZERO LLM)
  │   ├── /chapters/*
  │   ├── /quizzes/*
  │   ├── /progress/*
  │   ├── /search
  │   └── /access/*
  │
  └─ Phase 2 Routes (hybrid — Pro only)
      └── /hybrid/*
           └── hybrid_service.py
                └── Anthropic SDK → Claude Sonnet (claude-sonnet-4-6)
```

---

## Cost Analysis

| Feature | Model | Input Tokens | Output Tokens | Cost/Request |
|---------|-------|-------------|--------------|-------------|
| LLM Assessment | claude-sonnet-4-6 | ~1,200 | ~300 | ~$0.014 |
| Cross-Chapter Synthesis | claude-sonnet-4-6 | ~2,000 | ~500 | ~$0.024 |

**Monthly cost for 100 Pro users (50 requests/user):**
- Assessment: 100 × 50 × $0.014 = **$70/month**
- Synthesis: 100 × 50 × $0.024 = **$120/month**
- Revenue from 100 Pro users: 100 × $19.99 = **$1,999/month**
- **Margin: ~90%** even with heavy usage

---

## Risk Analysis

| Risk | Impact | Mitigation |
|------|--------|-----------|
| LLM API timeout | User sees 500 error | 30s FastAPI timeout; clear error message |
| Cost spike from heavy usage | Margin erosion | `hybrid_usage` table enables per-user throttling (future) |
| JSON parse failure from Claude | 500 error | try/except with JSON extraction logic in hybrid_service.py |

---

## Deliverables Checklist

- [x] `POST /hybrid/assess` implemented and tested
- [x] `POST /hybrid/synthesize` implemented and tested
- [x] `GET /hybrid/usage/{user_id}` implemented
- [x] `HybridUsage` model and migration added
- [x] Mock mode for demo without API key
- [x] Pro tier gate enforced (403 for free/premium)
- [x] Cost tracked per request in `hybrid_usage` table
- [x] Frontend: synthesis page at `/synthesis`
- [x] Frontend: assessment tab on chapter pages
- [x] Phase 1 routes remain zero-LLM (verified by audit)
