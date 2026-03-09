# Quickstart: Phase 1 ChatGPT App — Zero-Backend-LLM Course Companion

**Date**: 2026-03-09 | **Branch**: `1-phase1-chatgpt-app`

This guide validates the Phase 1 system is working end-to-end.
Run each step in order. All steps MUST pass before the feature is considered complete.

---

## Prerequisites

```bash
# Required tools
python --version        # Must be 3.11+
pip --version
git --version

# Required environment variables (copy from .env.example)
cp .env.example .env
# Fill in:
#   DATABASE_URL=postgresql+asyncpg://<neon-connection-string>
#   R2_ACCOUNT_ID=<cloudflare-account-id>
#   R2_ACCESS_KEY_ID=<r2-access-key>
#   R2_SECRET_ACCESS_KEY=<r2-secret>
#   R2_BUCKET_NAME=course-companion-content
```

---

## Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Expected output: All packages installed with no errors.

---

## Step 2: Run Database Migrations

```bash
cd backend
alembic upgrade head
```

Expected output:
```
Running upgrade -> <rev_id>, Create chapters, quizzes, content_sections tables
Running upgrade -> <rev_id>, Create user_progress, quiz_submissions tables
```

---

## Step 3: Seed Course Content

```bash
cd backend
python scripts/seed.py
```

Expected output:
```
✓ Uploading chapter content to Cloudflare R2...
✓ Seeded 5 chapters
✓ Seeded 5 quizzes (5 questions each)
✓ Indexed 50 content sections for search
Seeding complete.
```

---

## Step 4: Start the Backend Server

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

## Step 5: Verify Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "ok", "version": "1.0.0"}
```

---

## Step 6: Test Content Delivery (FR-001, US1)

```bash
curl -H "X-User-ID: test_user" http://localhost:8000/chapters/1
```

Expected: Full chapter JSON with `body` field (verbatim text from R2).
Must NOT contain any LLM-processed content.

```bash
# Test navigation
curl -H "X-User-ID: test_user" http://localhost:8000/chapters/1/next
# Expected: chapter 2 metadata

curl -H "X-User-ID: test_user" http://localhost:8000/chapters/1/previous
# Expected: {"is_boundary": true, "boundary_type": "first", "target": null}
```

---

## Step 7: Test Search / Grounded Q&A (FR-003, US2)

```bash
curl -H "X-User-ID: test_user" \
  "http://localhost:8000/search?q=What+is+an+MCP+server"
```

Expected: `sections` array with 3–5 results, each with `chapter_id`, `text`,
and `relevance_score`. `no_results: false`.

```bash
# Test no-results case
curl -H "X-User-ID: test_user" \
  "http://localhost:8000/search?q=banana+smoothie+recipe"
# Expected: {"no_results": true, "sections": [], "total": 0}
```

---

## Step 8: Test Rule-Based Quizzes (FR-004, FR-005, US3)

```bash
# Get quiz questions (answer key must NOT be in response)
curl -H "X-User-ID: test_user" http://localhost:8000/quizzes/chapter/1
# Expected: 5 questions with A/B/C/D options, NO "correct_option" field

# Submit answers
curl -X POST http://localhost:8000/quizzes/1/submit \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "answers": {"1":"A","2":"B","3":"C","4":"D","5":"A"}}'
# Expected: score, percentage, passed (true/false), per-question results with explanations

# Test incomplete submission
curl -X POST http://localhost:8000/quizzes/1/submit \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "answers": {"1":"A"}}'
# Expected: 400 error with missing question IDs
```

---

## Step 9: Test Progress Tracking (FR-006, US4)

```bash
# Mark chapter 1 complete
curl -X PUT http://localhost:8000/progress/test_user/chapters/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
# Expected: updated progress with completed_chapters: [1], streak >= 1

# Get progress
curl http://localhost:8000/progress/test_user
# Expected: completed_chapters: [1], current_streak: 1, course_completion_pct: 20.0

# Test unknown user (auto-create)
curl http://localhost:8000/progress/brand_new_user
# Expected: zero-state progress (not 404)
```

---

## Step 10: Test Freemium Gate (FR-007, US5)

```bash
# Free user accessing free content (should succeed)
curl "http://localhost:8000/access/check?user_id=test_user&resource=chapter_1"
# Expected: {"access": true}

# Free user accessing premium content (should be blocked)
curl "http://localhost:8000/access/check?user_id=test_user&resource=chapter_4"
# Expected: {"access": false, "reason": "premium_required", "upgrade_url": "..."}

# Verify chapter 4 returns 403 for free user
curl -H "X-User-ID: test_user" http://localhost:8000/chapters/4
# Expected: 403 with AccessDenied schema
```

---

## Step 11: Verify Zero-LLM Compliance (FR-010, SC-008)

```bash
# Audit: grep for any LLM client imports in backend source
grep -r "anthropic\|openai\|langchain\|litellm\|ollama" backend/app/ --include="*.py"
# Expected: NO matches (zero LLM calls in backend)
```

---

## Step 12: View OpenAPI Documentation

Open in browser: `http://localhost:8000/docs`

Verify:
- All 10 endpoints are listed
- Request/response schemas match `contracts/openapi.yaml`
- Try-it-out works for each endpoint

---

## Step 13: Run Tests

```bash
cd backend
pytest tests/ -v
```

Expected: All tests pass. No test should mock or call any LLM API.

---

## Validation Complete

If all 13 steps pass:
- ✅ Phase 1 backend is functional
- ✅ Zero-LLM compliance verified
- ✅ All 6 required features working
- ✅ Ready for ChatGPT App integration and Phase 2 planning
