# Tasks: Phase 2 — Hybrid Intelligence

## Phase 1 — Setup
- [ ] T001 Install anthropic SDK in backend/requirements.txt
- [ ] T002 Add ANTHROPIC_API_KEY to config.py and .env.example
- [ ] T003 Create migration 004_create_hybrid_usage_table.py

## Phase 2 — Backend Hybrid Routes
- [ ] T004 Create backend/app/models/hybrid_usage.py
- [ ] T005 Create backend/app/schemas/hybrid.py (request/response schemas)
- [ ] T006 Create backend/app/services/hybrid_service.py (Claude calls)
- [ ] T007 Create backend/app/routers/hybrid.py (2 endpoints)
- [ ] T008 Register hybrid router in main.py

## Phase 3 — Frontend
- [ ] T009 Add Assessment tab to frontend chapter page
- [ ] T010 Create frontend/src/app/synthesis/page.tsx
- [ ] T011 Add hybrid API calls to frontend/src/lib/api.ts
- [ ] T012 Add /synthesis link to Navbar

## Phase 4 — Polish
- [ ] T013 Run migration, test endpoints
- [ ] T014 Update README with Phase 2 docs
- [ ] T015 Push and commit
