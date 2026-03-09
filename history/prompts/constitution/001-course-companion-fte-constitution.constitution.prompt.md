---
id: 001
title: Course Companion FTE Constitution
stage: constitution
date: 2026-03-09
surface: agent
model: claude-sonnet-4-6
feature: none
branch: master
user: Asma kahn
command: /sp.constitution
labels: ["constitution","hackathon-4","zero-backend-llm","dual-frontend","phase-gated","agent-skills","cost-efficiency","spec-driven"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/001-course-companion-fte-constitution.constitution.prompt.md
tests:
  - N/A
---

## Prompt

@hackathon-4.md ko read karo aur full requirment ko follow karo aur /sp.constitution bnao project ki .specify/memory/constitution.md

## Response snapshot

Created the Course Companion FTE Constitution v1.0.0 at `.specify/memory/constitution.md`.

Constitution includes:
- 6 core principles derived from hackathon-4.md requirements
- Technology Stack table (all 8 Agent Factory layers)
- Development Workflow with deliverables checklist
- Governance section with amendment procedure and GOLDEN RULES

Principles defined:
1. Zero-Backend-LLM by Default (NON-NEGOTIABLE) — Phase 1 strict no-LLM-in-backend
2. Dual-Frontend Architecture — ChatGPT App (OpenAI Agents SDK) + Web App (Next.js)
3. Phase-Gated Feature Delivery — Phase 1 → Phase 2 (hybrid premium) → Phase 3 (full web)
4. Agent Skills as Procedural Knowledge Units — 4 required SKILL.md files
5. Cost Efficiency & Scalability — R2 + Neon + Fly.io, <$0.004/user/month (Phase 1)
6. Spec-Driven Development — spec → plan → tasks → implement

## Outcome

- ✅ Impact: Project constitution ratified at v1.0.0, all hackathon requirements encoded as non-negotiable principles
- 🧪 Tests: N/A (documentation artifact)
- 📁 Files: .specify/memory/constitution.md written (full content, no unresolved placeholders)
- 🔁 Next prompts: /sp.specify to create feature specs for Phase 1 features; /sp.plan for architecture planning
- 🧠 Reflection: All 6 hackathon-4.md requirements mapped to principles; disqualification triggers explicitly called out

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run /sp.specify for Phase 1 ChatGPT App feature
