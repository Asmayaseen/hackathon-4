from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import AsyncSessionLocal, engine
from app.routers import access, chapters, health, hybrid, progress, quizzes, search


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: verify DB connection
    async with AsyncSessionLocal() as session:
        await session.execute(__import__("sqlalchemy").text("SELECT 1"))
    yield
    # Shutdown: dispose engine
    await engine.dispose()


app = FastAPI(
    title="Course Companion FTE — Phase 1 + 2 API",
    description=(
        "**Phase 1** (Zero-Backend-LLM): Content, Quizzes, Progress, Search — ZERO LLM inference.\n\n"
        "**Phase 2** (Hybrid Intelligence): `/hybrid/*` routes use Claude Sonnet for Pro users only.\n\n"
        "Phase isolation: All Phase 1 routes remain deterministic. Only `/hybrid/*` calls LLMs."
    ),
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS — open in Phase 1 (tighten in Phase 2)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(health.router)
app.include_router(chapters.router)
app.include_router(search.router)
app.include_router(quizzes.router)
app.include_router(progress.router)
app.include_router(access.router)
app.include_router(hybrid.router)   # Phase 2 — Pro-gated hybrid intelligence
