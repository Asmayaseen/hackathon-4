<!--
SYNC IMPACT REPORT
==================
Version change: 0.0.0 (template) → 1.0.0 (initial ratification)
Modified principles: N/A (initial creation)
Added sections:
  - Core Principles (6 principles)
  - Technology Stack
  - Development Workflow
  - Governance
Templates requiring updates:
  ✅ .specify/templates/plan-template.md — Constitution Check gates align with principles below
  ✅ .specify/templates/spec-template.md — Scope/requirements aligned with Phase-gated delivery
  ✅ .specify/templates/tasks-template.md — Task categories reflect observability, versioning, cost tracking
Deferred TODOs: None — all placeholders resolved.
-->

# Course Companion FTE Constitution

## Core Principles

### I. Zero-Backend-LLM by Default (NON-NEGOTIABLE)

The backend MUST perform ZERO LLM inference in Phase 1. All reasoning, explanation,
tutoring, and adaptation is delegated entirely to ChatGPT. The backend is purely
deterministic: it serves content verbatim, grades quizzes by rule, tracks progress,
and enforces access control.

**Non-negotiable rules:**
- Backend MUST NOT contain any LLM API calls, RAG summarization, prompt orchestration,
  or agent loops in Phase 1.
- Content MUST be pre-generated and served verbatim from Cloudflare R2.
- Any violation of this principle in Phase 1 results in immediate disqualification.
- Hybrid (backend LLM calls) is ONLY permitted in Phase 2, gated behind premium tiers,
  user-initiated, feature-scoped, and cost-tracked.

**Rationale:** Near-zero marginal cost per user, predictable scaling to 100k+ users,
no vendor LLM cost risk for core delivery, and full auditability of educational content.

### II. Dual-Frontend Architecture

The system MUST expose two separate frontends sharing backend APIs but with independent
codebases: a ChatGPT App (OpenAI Agents SDK) and a Web App (Next.js / React).

**Non-negotiable rules:**
- Phase 1 & 2: ChatGPT App MUST be the primary frontend using OpenAI Agents SDK.
- Phase 3: A standalone Web App (Next.js) MUST be built with full LMS features.
- Both frontends MUST share the same FastAPI backend API contracts.
- Frontend codebases MUST remain separate; no shared source directories.
- The Web App MUST be responsive and production-grade.

**Rationale:** Maximises user reach (800M+ ChatGPT users) while providing a standalone
LMS dashboard. Separation prevents coupling and enables independent deployment.

### III. Phase-Gated Feature Delivery

Features MUST be delivered in strict phases. No Phase 2 or Phase 3 features may be
introduced before the prior phase is complete and validated.

**Phases:**
- **Phase 1** — Zero-Backend-LLM: Deterministic FastAPI + ChatGPT App. All 6 required
  features (Content Delivery, Navigation, Grounded Q&A, Rule-Based Quizzes, Progress
  Tracking, Freemium Gate) MUST be implemented.
- **Phase 2** — Hybrid Intelligence: Maximum 2 hybrid features, premium-gated,
  user-initiated, isolated API routes, cost-tracked. Allowed: Adaptive Learning Path,
  LLM-Graded Assessments, Cross-Chapter Synthesis, AI Mentor Agent.
- **Phase 3** — Full Web App: Next.js frontend + consolidated FastAPI backend with all
  features and LLM calls permitted.

**Non-negotiable rules:**
- Phase 2 hybrid features MUST be isolated in separate API routes from Phase 1.
- Hybrid features MUST NOT be auto-triggered or required for core UX.
- Cost per hybrid request MUST be tracked and documented.
- Phase 3 MUST include all 6 required features plus LLM backend calls.

**Rationale:** Enforces the Agent Factory Architecture principle: start Zero-LLM,
add hybrid only where value is demonstrably proven and cost-justified.

### IV. Agent Skills as Procedural Knowledge Units

All educational behaviours MUST be encoded as SKILL.md files. Each skill defines a
named, trigger-keyword-driven procedure that the Course Companion FTE executes
consistently.

**Required runtime skills (MUST be implemented):**
- `concept-explainer` — triggered by "explain", "what is", "how does"
- `quiz-master` — triggered by "quiz", "test me", "practice"
- `socratic-tutor` — triggered by "help me think", "I'm stuck"
- `progress-motivator` — triggered by "my progress", "streak", "how am I doing"

**Each SKILL.md MUST contain:** Metadata (name, description, trigger keywords),
Purpose, Workflow (step-by-step), Response Templates, and Key Principles/constraints.

**Rationale:** Skills encode the FTE's domain knowledge as specs, enabling instant
ramp-up, 99%+ consistency, and spec-driven quality control. The Spec IS the source code.

### V. Cost Efficiency & Scalability

Every architectural decision MUST be evaluated against unit cost economics. The system
MUST be designed to serve 10,000+ users at under $0.004 per user per month (Phase 1).

**Non-negotiable rules:**
- Phase 1 storage MUST use Cloudflare R2 ($0.015/GB + $0.36/M reads).
- Database MUST start on free tier (Neon / Supabase), scaling to $25/mo max for 10k users.
- Compute MUST be hosted on Fly.io or Railway (~$10/mo for 10k users).
- Phase 2 hybrid features MUST document estimated cost per request before implementation.
- Monetisation tiers MUST be implemented: Free ($0), Premium ($9.99/mo), Pro ($19.99/mo).
- No backend infrastructure decision that increases per-user cost above $0.01 (Phase 1)
  is permitted without explicit cost justification.

**Rationale:** The Digital FTE thesis requires 85–90% cost savings vs human tutors.
Predictable cost is a product feature, not just an operational concern.

### VI. Spec-Driven Development

All features MUST begin with a written specification. The spec is the authoritative
source of truth. Code is the artifact produced FROM the spec, not the other way around.

**Non-negotiable rules:**
- Every feature MUST have a `spec.md` before implementation begins.
- Every feature MUST have a `plan.md` (architecture) before tasks are written.
- Every feature MUST have a `tasks.md` with dependency-ordered, independently-testable
  tasks before implementation starts.
- No implementation MUST proceed without passing the Constitution Check in `plan.md`.
- APIs MUST be documented in OpenAPI/Swagger format.
- The ChatGPT App MUST ship with a valid YAML App Manifest.
- README MUST be complete, architecture diagram MUST be included as PNG/PDF,
  and a cost analysis document MUST be submitted.

**Rationale:** Agent Factory Architecture requires: Spec → General Agent (Claude Code)
manufactures → Custom Agent (Course Companion FTE). The spec is what scales quality.

## Technology Stack

| Layer | Technology | Phase |
|-------|-----------|-------|
| L0 | Agent Sandbox (gVisor) | Phase 2 & 3 |
| L1 | Apache Kafka | Phase 2 & 3 |
| L2 | Dapr + Workflows | Phase 2 & 3 |
| L3 | FastAPI (Python) | Phase 1, 2, & 3 |
| L4 | OpenAI Agents SDK | Phase 2 & 3 |
| L5 | Claude Agent SDK | Phase 2 & 3 |
| L6 | Runtime Skills + MCP | Phase 1, 2, & 3 |
| L7 | A2A Protocol | Phase 2 & 3 |

**Content Storage:** Cloudflare R2 (all phases)
**Database:** Neon or Supabase (all phases)
**Compute:** Fly.io or Railway (all phases)
**ChatGPT Frontend:** OpenAI Agents SDK (Phase 1 & 2)
**Web Frontend:** Next.js / React (Phase 3)
**Backend:** FastAPI (Python) — deterministic in Phase 1, hybrid in Phase 2 & 3
**LLM for Hybrid:** Claude Sonnet (Phase 2 & 3 only)

**Course Content:** Teams MUST choose ONE topic: AI Agent Development, Cloud-Native
Python, Generative AI Fundamentals, or Modern Python with Typing.

## Development Workflow

1. **Specify first** — Write `spec.md` capturing user stories, acceptance scenarios,
   and functional requirements before any code is written.
2. **Plan second** — Write `plan.md` with architecture decisions, technology choices,
   API contracts, and Constitution Check gates.
3. **Task breakdown** — Write `tasks.md` with dependency-ordered, phase-grouped,
   independently-testable tasks.
4. **Implement incrementally** — Complete Phase 1 fully before starting Phase 2.
   Validate each phase against the judging rubric before proceeding.
5. **Document continuously** — API docs (OpenAPI/Swagger), README, architecture
   diagram, and cost analysis MUST be maintained alongside code.
6. **Demo video** — A 5-minute MP4 walkthrough covering: Introduction (30s),
   Architecture (1m), Web Frontend Demo (1.5m), ChatGPT App Demo (1.5m),
   Phase 2 features (30s).

**Disqualification triggers (MUST avoid):**
- Any LLM API call in the backend during Phase 1.
- Missing any of the 6 required Phase 1 features.
- Hybrid features that are auto-triggered or required for free-tier UX.

**Deliverables checklist:**
- [ ] GitHub repo with complete codebase and README
- [ ] Architecture Diagram (PNG/PDF)
- [ ] Spec Document (Markdown)
- [ ] Cost Analysis (Markdown/PDF)
- [ ] Demo Video (MP4, 5 min)
- [ ] API Documentation (OpenAPI/Swagger)
- [ ] ChatGPT App Manifest (YAML)

## Governance

This constitution supersedes all other development practices for the Course Companion
FTE project. All team members MUST verify compliance with these principles before
merging any pull request.

**Amendment procedure:**
1. Propose amendment with written rationale referencing the judging rubric impact.
2. Increment `CONSTITUTION_VERSION` per semantic versioning:
   - MAJOR: Removal or redefinition of a core principle.
   - MINOR: New principle or material section added.
   - PATCH: Clarification, wording, or typo fix.
3. Update `LAST_AMENDED_DATE` to amendment date.
4. Propagate changes to all dependent templates and PHRs.
5. Document as an ADR if the amendment is architecturally significant.

**Compliance review:** Every `plan.md` MUST include a Constitution Check section
verifying all 6 principles. Any violation MUST be explicitly justified in a
Complexity Tracking table.

**Runtime guidance:** See `.specify/memory/constitution.md` (this file) as the
authoritative runtime reference for all development decisions.

**GOLDEN RULES:**
- Zero-Backend-LLM is the default. Hybrid intelligence MUST always be selective,
  justified, and premium.
- Your Spec is your Source Code. If you can describe the excellence you want,
  AI can build the Digital FTE to deliver it.

**Version**: 1.0.0 | **Ratified**: 2026-03-09 | **Last Amended**: 2026-03-09
