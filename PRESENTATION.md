# 🎓 Course Companion FTE — Presentation Script

## Slide 1 — Title
**"Course Companion FTE"**
*Panaversity Agent Factory Hackathon IV — 2026*
*By: Asma Yaseen*

> "Main aaj aapko ek aisa platform dikhane ja rahi hoon jo 10,000 students ko ek saath tutor kar sakta hai — sirf $16 per month mein."

---

## Slide 2 — Problem
**Masla kya hai?**

- Students ko 24/7 tutor chahiye hota hai
- Human tutors expensive hain — $20-50/hour
- AI tutors (ChatGPT directly) course content se bahar ja sakte hain
- Koi progress tracking nahi hoti
- Quizzes aur assessment mushkil hota hai

---

## Slide 3 — Solution
**Hamara Hal — Course Companion FTE**

✅ 24/7 available AI tutor
✅ Sirf course content pe grounded — koi hallucination nahi
✅ Automatic progress tracking + streaks
✅ Rule-based quizzes (no LLM needed)
✅ Full-text search across all chapters
✅ Free + Premium tiers

---

## Slide 4 — Architecture
**Zero-Backend-LLM Architecture**

```
Student → Next.js App → FastAPI Backend → Neon Database
                    ↕
              ChatGPT App (all AI here)
              4 Skills: Explain, Quiz, Socratic, Motivate
```

**Key Innovation:** Backend mein ZERO AI calls — sirf ChatGPT App mein intelligence hai
**Result:** $0.002 per user per month

---

## Slide 5 — Live Demo
**Demo sequence:**

1. Home page dikhao → "5 chapters, 25 questions, $0 LLM cost"
2. Chapters → Chapter 1 open karo → content padho
3. Quiz → attempt karo → score dekho
4. Progress → streak + completion bar
5. Search → "What is an AI agent?" search karo

---

## Slide 6 — Features
**5 Core Features**

| # | Feature | Technology |
|---|---------|-----------|
| 1 | 📚 Course Content | Next.js + FastAPI + PostgreSQL |
| 2 | 🧠 Smart Search | PostgreSQL Full-Text Search |
| 3 | ✅ Auto-Graded Quizzes | Rule-based grading |
| 4 | 🔥 Streak Tracking | UTC date comparison logic |
| 5 | 🤖 AI Teaching Skills | OpenAI Agents SDK + SKILL.md |

---

## Slide 7 — Tech Stack
**Technology Choices**

| Layer | Tech | Why |
|-------|------|-----|
| Frontend | Next.js 14 | Fast, SEO, TypeScript |
| Backend | FastAPI | Async, Python, Fast |
| Database | Neon PostgreSQL | Free tier, Serverless |
| Search | FTS (tsvector) | No LLM needed |
| AI App | OpenAI Agents SDK | SKILL.md support |

---

## Slide 8 — Cost
**Kitna Sasta Hai?**

| Platform | Users | Cost/Month |
|----------|-------|-----------|
| Traditional LLM | 10,000 | ~$2,000+ |
| Course Companion | 10,000 | ~$16–41 |
| **Savings** | | **98% cheaper** |

---

## Slide 9 — SDD Process
**Spec-Driven Development**

Hamne poora project structured process se banaya:

1. 📋 Constitution (6 principles)
2. 📝 Specification (5 user stories)
3. 🏗️ Architecture Plan
4. ✅ 60 Tasks (sab complete)
5. 💻 Implementation

---

## Slide 10 — GitHub
**Code dekho:**

🔗 github.com/Asmayaseen/hackathon-4

- 94 files
- 10,000+ lines of code
- Full test suite
- OpenAPI documentation
- Complete SDD artifacts

---

## Closing — Thank You

> "Course Companion FTE Phase 1 complete hai. Phase 2 mein hybrid LLM premium features aayenge. Phase 3 mein full production deployment hoga."

**"Shukriya! Koi sawaal?"**

---

## Demo Video Script (5 minutes)

```
00:00 — "Assalam o Alaikum, main Asma hoon. Aaj main Course Companion FTE present kar rahi hoon."
00:15 — Home page dikhao
00:45 — Chapters page → Chapter 1 open karo
01:30 — Quiz attempt karo (2-3 questions)
02:30 — Progress page → streak dikhao
03:00 — Search page → search karo
03:30 — Backend API docs → http://localhost:8000/docs
04:00 — GitHub repo dikhao → code structure
04:30 — "Ye zero LLM backend hai, koi AI call nahi — sirf $16/month mein 10,000 users"
05:00 — "Thank you!"
```
