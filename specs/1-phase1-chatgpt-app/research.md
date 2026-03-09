# Research: Phase 1 ChatGPT App — Zero-Backend-LLM Course Companion

**Date**: 2026-03-09
**Branch**: `1-phase1-chatgpt-app`
**Status**: Complete — all NEEDS CLARIFICATION resolved

---

## Decision 1: Python Version & FastAPI Setup

**Decision**: Python 3.11+ with FastAPI 0.110+, Uvicorn, and Pydantic v2.

**Rationale**:
- Python 3.11 is the current LTS with best performance (15–60% faster than 3.10).
- FastAPI auto-generates OpenAPI/Swagger docs (FR-009) from type hints — zero extra config.
- Pydantic v2 provides 5–10x faster validation than v1, important for <500ms SLOs.
- Uvicorn is the standard ASGI server for FastAPI production deployments.

**Alternatives considered**:
- Django REST Framework: heavier, slower startup, overkill for this API surface.
- Flask: no native async, no auto-OpenAPI, requires manual serialisation.

---

## Decision 2: Database — Neon (PostgreSQL) over Supabase

**Decision**: Neon (serverless PostgreSQL) for progress and quiz data storage.

**Rationale**:
- Free tier includes 0.5 GB storage and 10 branches — sufficient for Phase 1.
- Neon's serverless scaling matches the 1,000 concurrent user SLO (SC-006).
- asyncpg driver enables fully async DB calls keeping FastAPI non-blocking.
- SQLModel (built on Pydantic + SQLAlchemy) provides typed ORM without boilerplate.
- Cost: $0 (free tier) for <10k users, $19/mo for scale — within $41/month budget (SC-007).

**Alternatives considered**:
- Supabase: more features but heavier, includes auth we don't need in Phase 1.
- SQLite: no concurrent write support, not suitable for 1,000+ concurrent users.
- Redis: appropriate for cache layer (future), not suitable as primary store.

---

## Decision 3: Cloudflare R2 — Content Storage Pattern

**Decision**: Chapter content stored as JSON files in R2; accessed via Cloudflare R2 SDK
(boto3-compatible S3 API). Content indexed at deploy time into PostgreSQL ContentSection
table for search.

**Rationale**:
- R2 has zero egress fees (unlike AWS S3), critical for cost control (SC-007).
- JSON files per chapter allow verbatim serving (FR-001) with no transformation.
- Pre-indexing content sections into Postgres at deploy time enables fast keyword
  search without R2 reads per query (SC-002 <1s search).
- $0.015/GB storage + $0.36/M reads → ~$5/month for 10k users (within budget).

**Alternatives considered**:
- Serving directly from R2 presigned URLs: exposes R2 directly, no access control.
- Storing content in PostgreSQL: content is large (MB), inflates DB cost unnecessarily.
- AWS S3: egress fees would violate cost budget at scale.

---

## Decision 4: Search Implementation — Keyword Full-Text Search (Phase 1)

**Decision**: PostgreSQL full-text search (tsvector/tsquery) on ContentSection table.
Semantic search (pgvector + embeddings) deferred to Phase 2 as a stretch goal.

**Rationale**:
- Spec assumption: keyword search is minimum viable for Phase 1.
- PostgreSQL FTS is deterministic (zero LLM calls, FR-010 compliant).
- tsvector indices on chapter content provide <100ms search (within SC-002 <1s SLO).
- No additional infrastructure required — reuses existing Neon PostgreSQL.
- Covers the "AI Agent Development" topic domain well as technical terms are distinctive.

**Alternatives considered**:
- Elasticsearch: overkill, adds ~$30/mo infrastructure, violates cost budget.
- pgvector (embeddings): requires embedding model calls — still zero-LLM compliant but
  adds complexity; saved for Phase 2 hybrid upgrade.
- Meilisearch: self-hosted, adds another service to manage.

---

## Decision 5: User Identity — Header-Based User ID (No Auth Phase 1)

**Decision**: User identity passed as `X-User-ID` header from ChatGPT App. No JWT or
session auth in Phase 1. OpenAI Agents SDK injects the authenticated user's identifier.

**Rationale**:
- Spec assumption confirmed: no separate auth flow in Phase 1.
- OpenAI's ChatGPT App platform provides authenticated user context — the App Manifest
  can map the ChatGPT user to a stable user ID passed to the backend.
- Simplifies backend significantly: no auth middleware, no token validation, no refresh
  tokens — all out of scope for Phase 1.
- Freemium tier stored in UserProgress record, set at user creation (default: free).

**Alternatives considered**:
- JWT auth: overly complex for Phase 1, adds attack surface, not required by rubric.
- API key per user: same complexity without the security model of JWT.

---

## Decision 6: ChatGPT App Architecture — OpenAI Agents SDK

**Decision**: Build ChatGPT App using OpenAI Agents SDK with:
- A custom GPT (ChatGPT App) configured via YAML manifest.
- Actions defined pointing to the FastAPI backend endpoints.
- System prompt embedding all 4 SKILL.md contents as grounding instructions.
- Hosted on the same FastAPI backend — manifest served at `/chatgpt-manifest.yaml`.

**Rationale**:
- OpenAI Agents SDK is the required technology per constitution (Phase 1 & 2).
- YAML manifest + actions = declarative ChatGPT App definition (FR-011).
- System prompt carries SKILL.md content, giving ChatGPT its procedural knowledge.
- Backend serves the manifest so it's version-controlled alongside API code.

**Alternatives considered**:
- Standalone GPT Builder (no-code): insufficient control over system prompt and actions.
- Custom ChatGPT plugin (deprecated): replaced by Agents SDK.

---

## Decision 7: Deployment — Fly.io

**Decision**: FastAPI backend deployed to Fly.io using Docker. Single `fly.toml` config.

**Rationale**:
- Fly.io free tier: 3 shared-CPU-1x VMs (256 MB RAM each) — sufficient for Phase 1.
- $10/month for 10k users is within the $41/month infrastructure budget.
- Native Docker support; zero vendor-specific code.
- Automatic TLS/SSL, global edge network matches SC-001 (<2s worldwide access).

**Alternatives considered**:
- Railway: similar pricing but less control over scaling.
- AWS Lambda: cold starts conflict with SC-001 (<2s) SLO.
- Render: free tier sleeps on inactivity — unacceptable for 24/7 SLO.

---

## Decision 8: Course Content — AI Agent Development (Option A)

**Decision**: Course content covers **AI Agent Development**: Claude Agent SDK concepts,
MCP (Model Context Protocol), Agent Skills, and Agent Factory Architecture.

**Rationale**:
- Directly aligned with the Panaversity hackathon domain (Agent Factory).
- Instructors can author content drawing directly from the hackathon specification.
- Most differentiated vs generic Python/AI courses — unique value proposition.
- Content pre-exists in the hackathon documentation — low authoring effort.

**Minimum content required for Phase 1**:
- 5+ chapters (3 free + 2+ premium) covering: Agent Basics, Claude SDK, MCP, Skills, A2A.
- 1 quiz per chapter (5 questions each, multiple choice).
- Content sections indexed for search (~10 sections per chapter).

---

## Resolved Assumptions

| Assumption | Resolved Value |
|------------|---------------|
| Auth mechanism | X-User-ID header (no JWT in Phase 1) |
| Course topic | AI Agent Development (Option A) |
| Search type | PostgreSQL full-text search (Phase 1) |
| DB provider | Neon (serverless PostgreSQL) |
| Compute | Fly.io (Docker) |
| User tier default | Free (upgrades set manually in Phase 1) |
| Streak timezone | UTC date |
| Content format | JSON files in Cloudflare R2 |
