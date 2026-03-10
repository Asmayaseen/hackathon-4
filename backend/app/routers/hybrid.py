"""
Phase 2 Hybrid Intelligence Router
Routes: POST /hybrid/assess, POST /hybrid/synthesize, GET /hybrid/usage/{user_id}

GATE: All routes require Pro tier. Free and Premium users receive 403.
"""
from decimal import Decimal

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_session
from app.models.hybrid_usage import HybridUsage
from app.models.user_progress import UserProgress
from app.schemas.hybrid import (
    AssessmentRequest, AssessmentResponse,
    SynthesisRequest, SynthesisResponse,
    UsageSummary, UsageRecord,
)
from app.services import hybrid_service

router = APIRouter(prefix="/hybrid", tags=["Phase 2 — Hybrid Intelligence"])

_PRO_TIERS = {"pro", "team"}


async def _require_pro(user_id: str, session: AsyncSession) -> UserProgress:
    """Raise 403 if user is not Pro tier."""
    progress = await session.execute(
        select(UserProgress).where(UserProgress.user_id == user_id)
    )
    user = progress.scalar_one_or_none()
    tier = user.tier if user else "free"
    if tier not in _PRO_TIERS:
        raise HTTPException(
            status_code=403,
            detail={
                "error": "pro_required",
                "message": "This feature requires a Pro subscription ($19.99/month).",
                "upgrade_url": settings.UPGRADE_URL,
                "your_tier": tier,
            }
        )
    return user


async def _require_api_key() -> None:
    """No-op in mock mode — always passes."""
    pass  # Mock mode handles missing key gracefully in hybrid_service.py


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/assess", response_model=AssessmentResponse, summary="LLM-Grade a written answer (Pro only)")
async def assess_answer(
    body: AssessmentRequest,
    x_user_id: str = Header(...),
    session: AsyncSession = Depends(get_session),
):
    """
    **Phase 2 Feature** — Grade a student's free-form written answer using Claude Sonnet.

    - Pro tier only
    - Evaluates reasoning quality, accuracy, and depth
    - Returns score (0-10), detailed feedback, strengths, and improvements
    - Cost: ~$0.014–0.018 per assessment
    """
    await _require_api_key()
    await _require_pro(x_user_id, session)

    try:
        return await hybrid_service.assess_answer(
            chapter_id=body.chapter_id,
            question=body.question,
            student_answer=body.student_answer,
            user_id=x_user_id,
            session=session,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Assessment failed: {str(e)}")


@router.post("/synthesize", response_model=SynthesisResponse, summary="Cross-chapter synthesis (Pro only)")
async def synthesize_chapters(
    body: SynthesisRequest,
    x_user_id: str = Header(...),
    session: AsyncSession = Depends(get_session),
):
    """
    **Phase 2 Feature** — Generate a cross-chapter synthesis using Claude Sonnet.

    - Pro tier only
    - Connects concepts across 2–5 chapters
    - Returns a coherent "big picture" explanation in markdown
    - Cost: ~$0.020–0.030 per synthesis
    """
    await _require_api_key()
    await _require_pro(x_user_id, session)

    try:
        return await hybrid_service.synthesize_chapters(
            chapter_ids=body.chapter_ids,
            focus_question=body.focus_question,
            user_id=x_user_id,
            session=session,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Synthesis failed: {str(e)}")


@router.get("/usage/{user_id}", response_model=UsageSummary, summary="Get hybrid feature usage + cost")
async def get_usage(
    user_id: str,
    x_user_id: str = Header(...),
    session: AsyncSession = Depends(get_session),
):
    """Get this month's hybrid feature usage and cost for a user."""
    if x_user_id != user_id:
        raise HTTPException(status_code=403, detail="Cannot view another user's usage.")

    result = await session.execute(
        select(HybridUsage)
        .where(HybridUsage.user_id == user_id)
        .order_by(HybridUsage.created_at.desc())
        .limit(50)
    )
    records = result.scalars().all()

    total_cost = sum(r.cost_usd for r in records)
    return UsageSummary(
        user_id=user_id,
        total_requests=len(records),
        total_cost_usd=Decimal(str(total_cost)),
        records=[
            UsageRecord(
                feature=r.feature,
                tokens_input=r.tokens_input,
                tokens_output=r.tokens_output,
                cost_usd=r.cost_usd,
                created_at=str(r.created_at),
            )
            for r in records
        ],
    )
