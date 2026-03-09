# Course Companion FTE — Panaversity Agent Factory Hackathon IV

A Digital Full-Time Equivalent (FTE) educational tutor for the **AI Agent Development** course.
Available 24/7, tutoring thousands of students simultaneously at ~$0.25 per session.

## Architecture

```
Student
  ↓
ChatGPT App (OpenAI Agents SDK)   ← ALL reasoning, tutoring, explanation
  ↓
FastAPI Backend (Python 3.11)      ← ZERO LLM inference — deterministic only
  ├── Cloudflare R2               ← Chapter content (verbatim storage)
  └── Neon PostgreSQL             ← Progress, quizzes, user data
```

**Phase 1**: Zero-Backend-LLM (this implementation)
**Phase 2**: Hybrid Intelligence (premium features — coming)
**Phase 3**: Next.js Web App (coming)

## Features (Phase 1)

| Feature | Backend | ChatGPT |
|---------|---------|---------|
| Content Delivery | Serves verbatim from R2 | Explains, summarises |
| Navigation | Next/previous chapter | Suggests optimal path |
| Grounded Q&A | Returns relevant sections | Answers using content only |
| Rule-Based Quizzes | Grades with answer key | Presents, encourages |
| Progress Tracking | Stores completion, streaks | Celebrates, motivates |
| Freemium Gate | Checks access rights | Explains premium gracefully |

## Quick Start

### Prerequisites

- Python 3.11+
- Neon PostgreSQL account (free tier)
- Cloudflare R2 account (free tier)
- Fly.io account (free tier)

### Local Development

```bash
# 1. Clone and set up
git clone <repo-url>
cd hackathon-4/backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your Neon DATABASE_URL and R2 credentials

# 4. Run migrations
alembic upgrade head

# 5. Seed course content
python scripts/seed.py

# 6. Start server
uvicorn app.main:app --reload --port 8000

# 7. View API docs
open http://localhost:8000/docs
```

### Run Tests

```bash
cd backend
pytest tests/ -v
```

### Zero-LLM Compliance Check

```bash
grep -r "anthropic\|openai\|langchain\|litellm\|ollama" backend/app/ --include="*.py"
# Expected: no output (zero violations)
```

## Project Structure

```
hackathon-4/
├── backend/                    # FastAPI Python backend
│   ├── app/
│   │   ├── main.py            # App entry point
│   │   ├── config.py          # Environment settings
│   │   ├── database.py        # Async PostgreSQL connection
│   │   ├── r2_client.py       # Cloudflare R2 client
│   │   ├── models/            # SQLModel database models
│   │   ├── schemas/           # Pydantic response schemas
│   │   ├── routers/           # FastAPI route handlers
│   │   └── services/          # Business logic layer
│   ├── migrations/            # Alembic migrations
│   ├── scripts/               # Seed + upload scripts
│   ├── tests/                 # pytest test suite
│   └── docs/                  # Zero-LLM audit, cost analysis
├── chatgpt-app/               # ChatGPT App (Phase 1 & 2 frontend)
│   ├── manifest.yaml          # OpenAI Agents SDK manifest
│   └── skills/                # SKILL.md procedural knowledge files
│       ├── concept-explainer.md
│       ├── quiz-master.md
│       ├── socratic-tutor.md
│       └── progress-motivator.md
├── specs/                     # Spec-Driven Development artifacts
│   └── 1-phase1-chatgpt-app/
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       ├── research.md
│       ├── data-model.md
│       ├── contracts/openapi.yaml
│       └── quickstart.md
└── fly.toml                   # Fly.io deployment config
```

## API Documentation

OpenAPI spec: [`specs/1-phase1-chatgpt-app/contracts/openapi.yaml`](specs/1-phase1-chatgpt-app/contracts/openapi.yaml)

Interactive docs (when running locally): http://localhost:8000/docs

## Course Content

**Topic**: AI Agent Development (Option A)
- Chapter 1: Introduction to AI Agents (free)
- Chapter 2: Claude Agent SDK (free)
- Chapter 3: Model Context Protocol — MCP (free)
- Chapter 4: Agent Skills and SKILL.md (premium)
- Chapter 5: A2A Protocol and Multi-Agent Systems (premium)

## Cost Analysis

See [`backend/docs/cost-analysis.md`](backend/docs/cost-analysis.md) for full breakdown.

**Phase 1 total cost for 10,000 monthly active users: $16–$41/month**
Cost per user: $0.002–$0.004/month

## Architecture Diagram

![Architecture](docs/architecture.png)
*(diagram to be added)*

## Spec-Driven Development

This project was built using the Agent Factory SDD workflow:
1. `/sp.constitution` — Project principles
2. `/sp.specify` — Feature requirements
3. `/sp.plan` — Architecture design
4. `/sp.tasks` — Implementation tasks
5. `/sp.implement` — Code generation

## Team

Panaversity Agent Factory Hackathon IV — 2026
