# 🎓 Course Companion FTE — Panaversity Agent Factory Hackathon IV

> **Digital Full-Time Equivalent Tutor** — AI-powered course companion that teaches 10,000 students simultaneously at near-zero cost.

---

## 🏆 What We Built

**Course Companion FTE** is a complete educational platform for the *AI Agent Development* course. It combines:
- A **Next.js Web App** for students to read, learn, and take quizzes
- A **FastAPI Backend** with zero LLM inference (all reasoning done by ChatGPT)
- A **ChatGPT App** (OpenAI Agents SDK) with 4 AI teaching skills
- **Neon PostgreSQL** for progress tracking and full-text search

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 📚 5 Chapters | Full AI Agent Development course content |
| 🧠 Smart Search | PostgreSQL full-text search — no LLM needed |
| ✅ Quizzes | 25 questions with explanations, auto-graded |
| 🔥 Streak Tracking | Daily learning streaks to motivate students |
| 🔒 Freemium | Chapters 1–3 free, 4–5 premium |
| 🤖 4 AI Skills | Explain, Quiz, Socratic, Motivate |
| 💰 $0 LLM Cost | Zero backend LLM calls in Phase 1 |

---

## 🏗️ Architecture

```
Student Browser
      ↓
Next.js Frontend (localhost:3001)
      ↓
FastAPI Backend (localhost:8000)   ← ZERO LLM — deterministic only
      ├── Neon PostgreSQL          ← Progress, Quizzes, Full-Text Search
      └── Chapter Content (DB)    ← Course material stored & served

ChatGPT App (OpenAI Agents SDK)   ← ALL AI reasoning lives here
      └── 4 Skills (SKILL.md)     ← concept-explainer, quiz-master,
                                     socratic-tutor, progress-motivator
```

### Zero-Backend-LLM Principle
The backend performs **ZERO** AI/LLM inference. All intelligence lives in the ChatGPT App. This means:
- Backend cost = ~$16/month for 10,000 users
- No API rate limits
- Fully deterministic, testable backend

---

## 🖥️ Screenshots & Demo

### Home Page
- Hero section with course overview
- 5 chapters, 25 quiz questions, $0 LLM cost stats
- Course outline with tier badges

### Chapters Page
- All 5 chapters listed with free/premium badges
- Click any chapter to read full content

### Quiz Page
- One question at a time
- Answer all questions → Submit → Get score + explanations
- Try again option

### Progress Page
- Course completion percentage bar
- Daily streak tracker 🔥
- Chapter-by-chapter breakdown with quiz scores

### Search Page
- Full-text search across all chapters
- Relevance score for each result
- Grounded in course material only

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS |
| Backend | Python 3.11, FastAPI 0.110 |
| Database | Neon PostgreSQL (async + FTS) |
| ORM | SQLModel + Alembic migrations |
| AI App | OpenAI Agents SDK (ChatGPT) |
| Search | PostgreSQL tsvector/tsquery |
| Storage | Cloudflare R2 (optional) |

---

## 📁 Project Structure

```
hackathon-4/
├── frontend/                   # Next.js 14 Web App
│   ├── src/app/
│   │   ├── page.tsx            # Landing page
│   │   ├── chapters/           # Chapter list + detail + quiz
│   │   ├── progress/           # Progress dashboard
│   │   └── search/             # Full-text search
│   └── src/components/
│       ├── layout/Navbar.tsx
│       └── ui/SimpleMarkdown.tsx
│
├── backend/                    # FastAPI Python Backend
│   ├── app/
│   │   ├── routers/            # chapters, quizzes, progress, search, access, health
│   │   ├── services/           # content, quiz, progress, search, access
│   │   ├── models/             # Chapter, Quiz, UserProgress, ContentSection
│   │   └── schemas/            # Pydantic response schemas
│   ├── migrations/             # Alembic (3 migrations)
│   ├── scripts/seed.py         # Seeds 5 chapters + 25 questions
│   └── tests/                  # pytest test suite (5 test files)
│
├── chatgpt-app/                # ChatGPT App (OpenAI Agents SDK)
│   ├── manifest.yaml           # App definition + 10 API actions
│   └── skills/
│       ├── concept-explainer.md
│       ├── quiz-master.md
│       ├── socratic-tutor.md
│       └── progress-motivator.md
│
└── specs/                      # Spec-Driven Development artifacts
    └── 1-phase1-chatgpt-app/
        ├── spec.md
        ├── plan.md
        ├── tasks.md (60 tasks ✅)
        ├── data-model.md
        └── contracts/openapi.yaml
```

---

## ⚡ Quick Start (Local)

```bash
# 1. Clone
git clone https://github.com/Asmayaseen/hackathon-4.git
cd hackathon-4/backend

# 2. Install
pip install -r requirements.txt

# 3. Setup .env
cp .env.example .env
# Add your Neon DATABASE_URL

# 4. Run migrations + seed
alembic upgrade head
python scripts/seed.py

# 5. Start backend
uvicorn app.main:app --reload --port 8000

# 6. Start frontend (new terminal)
cd ../frontend
npm install
npm run dev
# Open http://localhost:3001
```

---

## 💡 Course Content (5 Chapters)

1. **Introduction to AI Agents** *(Free)* — What agents are, reasoning loops, types
2. **Claude Agent SDK** *(Free)* — Tools, memory, multi-turn conversations
3. **Model Context Protocol (MCP)** *(Free)* — Universal standard for agent tools
4. **Agent Skills and SKILL.md** *(Premium)* — Procedural knowledge units
5. **A2A Protocol & Multi-Agent Systems** *(Premium)* — Agent-to-agent communication

---

## 💰 Cost Analysis

| Users/month | Estimated Cost |
|-------------|---------------|
| 1,000 | ~$5/month |
| 10,000 | ~$16–41/month |
| 100,000 | ~$120/month |

**Cost per user: $0.002–$0.004/month** — 500x cheaper than traditional LLM-per-request

---

## 🔍 Zero-LLM Audit

```bash
grep -r "anthropic\|openai\|langchain\|litellm" backend/app/ --include="*.py"
# Result: No output = ZERO violations ✅
```

---

## 📋 Spec-Driven Development Process

Built using Agent Factory SDD workflow:

```
/sp.constitution → /sp.specify → /sp.plan → /sp.tasks → /sp.implement
```

| Artifact | File |
|----------|------|
| Constitution | `.specify/memory/constitution.md` |
| Specification | `specs/1-phase1-chatgpt-app/spec.md` |
| Architecture Plan | `specs/1-phase1-chatgpt-app/plan.md` |
| Tasks (60 total) | `specs/1-phase1-chatgpt-app/tasks.md` |
| OpenAPI Contract | `specs/1-phase1-chatgpt-app/contracts/openapi.yaml` |

---

## 👩‍💻 Built By

**Asma Yaseen** — Panaversity Agent Factory Hackathon IV — 2026

---

## 📄 License

MIT License — Open source for educational use.
