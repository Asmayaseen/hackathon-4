# Feature Specification: Phase 2 — Hybrid Intelligence (Premium)

**Feature Branch**: `2-phase2-hybrid-intelligence`
**Created**: 2026-03-09
**Status**: Active
**Builds On**: Phase 1 (branch: 1-phase1-chatgpt-app)

---

## Overview

Phase 2 adds **selective backend LLM intelligence** for premium users only.
Two hybrid features are added — cleanly isolated from Phase 1 deterministic logic.

**Chosen Hybrid Features:**
- **B. LLM-Graded Assessments** — Free-form written answers graded by Claude Sonnet
- **C. Cross-Chapter Synthesis** — Concepts connected across chapters by Claude Sonnet

All Phase 1 features remain zero-LLM. Hybrid features are:
- Premium-gated (Pro tier only: $19.99/month)
- User-initiated (never auto-triggered)
- Isolated to separate API routes (`/hybrid/*`)
- Cost-tracked per user per request

---

## User Story 1 — LLM-Graded Assessments (Priority: P1)

A Pro-tier student finishes reading a chapter and wants to prove deep understanding.
Instead of multiple-choice, they type a free-form written answer explaining a concept.
The backend sends the answer + original content to Claude Sonnet, which evaluates:
reasoning quality, accuracy, completeness — and returns detailed feedback.

**Why LLM is necessary:** Rule-based grading cannot evaluate reasoning, explanation quality,
or the student's ability to synthesize ideas in their own words.

**Independent Test:** A Pro student submits "Explain what an AI agent is in your own words."
The system returns a score (0-10), feedback on strengths, and areas for improvement.

**Acceptance Scenarios:**

1. **Given** a Pro user submits a written answer, **When** `POST /hybrid/assess` is called,
   **Then** Claude evaluates it and returns score + feedback within 10 seconds.
2. **Given** a Free/Premium user calls `/hybrid/assess`, **When** access is checked,
   **Then** a 403 response with upgrade prompt is returned.
3. **Given** a Pro user submits an empty answer, **When** validated,
   **Then** a 400 error is returned without making an LLM call.
4. **Given** LLM call costs are tracked, **When** assessment completes,
   **Then** tokens used and cost are logged to `hybrid_usage` table.

---

## User Story 2 — Cross-Chapter Synthesis (Priority: P2)

A Pro-tier student has completed multiple chapters and wants to understand how concepts
connect. They request a "synthesis" — Claude Sonnet reads relevant sections from multiple
chapters and generates a connected "big picture" explanation showing how AI Agents, MCP,
Skills, and A2A all relate to each other.

**Why LLM is necessary:** Multi-document reasoning and concept connection requires
understanding relationships across chapters — impossible with keyword search alone.

**Independent Test:** A Pro student requests synthesis for chapters 1-3. The system returns
a connected explanation linking agents → SDK → MCP in a coherent narrative.

**Acceptance Scenarios:**

1. **Given** a Pro user requests synthesis of chapters 1,2,3, **When** `POST /hybrid/synthesize`,
   **Then** Claude returns a connected explanation within 15 seconds.
2. **Given** a Free user calls `/hybrid/synthesize`, **When** access checked,
   **Then** 403 with upgrade message is returned.
3. **Given** chapter IDs include a non-existent chapter, **When** validated,
   **Then** 404 is returned without making an LLM call.
4. **Given** more than 5 chapters requested, **When** validated,
   **Then** 400 is returned (cost guard: max 5 chapters per synthesis).

---

## Functional Requirements

### FR1 — Hybrid Assessment Endpoint
- `POST /hybrid/assess`
- Input: `chapter_id`, `question`, `student_answer` (max 1000 chars)
- Output: `score` (0-10), `feedback`, `strengths`, `improvements`, `tokens_used`, `cost_usd`
- LLM: Claude Sonnet (`claude-sonnet-4-6`)
- Context: Chapter content sent as grounding material
- Pro tier only

### FR2 — Cross-Chapter Synthesis Endpoint
- `POST /hybrid/synthesize`
- Input: `chapter_ids` (list, 2-5 chapters), `focus_question` (optional)
- Output: `synthesis` (markdown text), `chapters_used`, `tokens_used`, `cost_usd`
- LLM: Claude Sonnet (`claude-sonnet-4-6`)
- Context: Content sections from all requested chapters
- Pro tier only

### FR3 — Cost Tracking
- Every hybrid API call logs to `hybrid_usage` table:
  `user_id`, `feature`, `tokens_input`, `tokens_output`, `cost_usd`, `created_at`
- Per-user monthly cost viewable via `GET /hybrid/usage/{user_id}`

### FR4 — Tier Gate
- Free → 403 on all `/hybrid/*` routes
- Premium → 403 on all `/hybrid/*` routes
- Pro → full access

### FR5 — Frontend Integration
- Phase 2 Assessment tab on each chapter page (Pro badge)
- Synthesis page at `/synthesis` (Pro badge)
- Cost display: "This used ~$0.018 of your Pro quota"

---

## Key Entities

### HybridUsage
- `id`, `user_id`, `feature` (assess/synthesize), `chapter_ids`, `tokens_input`,
  `tokens_output`, `cost_usd`, `created_at`

### AssessmentRequest
- `chapter_id`, `question`, `student_answer`

### AssessmentResponse
- `score` (0-10), `feedback`, `strengths[]`, `improvements[]`, `tokens_used`, `cost_usd`

### SynthesisRequest
- `chapter_ids[]`, `focus_question` (optional)

### SynthesisResponse
- `synthesis` (markdown), `chapters_used[]`, `tokens_used`, `cost_usd`

---

## Success Criteria

1. LLM assessment returns meaningful feedback within 10 seconds for 95% of requests
2. Cross-chapter synthesis returns coherent explanation within 15 seconds
3. Zero hybrid LLM calls for Free/Premium users (gate enforced 100%)
4. Cost per assessment ≤ $0.02; cost per synthesis ≤ $0.03
5. All hybrid costs tracked — per-user monthly report available
6. Phase 1 zero-LLM features remain completely unaffected

---

## Phase Isolation Rules

| Route | Phase | LLM |
|-------|-------|-----|
| `/chapters/*` | Phase 1 | ❌ Never |
| `/quizzes/*` | Phase 1 | ❌ Never |
| `/progress/*` | Phase 1 | ❌ Never |
| `/search` | Phase 1 | ❌ Never |
| `/hybrid/assess` | Phase 2 | ✅ Pro only |
| `/hybrid/synthesize` | Phase 2 | ✅ Pro only |
| `/hybrid/usage/*` | Phase 2 | ❌ Never (tracking only) |
