"""
Phase 3 — Admin Stats Router
GET /admin/stats — platform-level statistics for the admin panel.
No LLM calls — purely aggregate DB queries.
"""
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.chapter import Chapter
from app.models.hybrid_usage import HybridUsage
from app.models.quiz_submission import QuizSubmission
from app.models.user_progress import UserProgress

router = APIRouter(prefix="/admin", tags=["Phase 3 — Admin"])


@router.get("/stats", summary="Platform admin statistics")
async def get_admin_stats(session: AsyncSession = Depends(get_session)):
    """
    Returns aggregate platform statistics for the admin dashboard.
    Phase 3 feature — no LLM calls.
    """
    # Total users
    users_result = await session.execute(select(func.count(UserProgress.user_id)))
    total_users = users_result.scalar() or 0

    # Total chapters
    chapters_result = await session.execute(select(func.count(Chapter.id)))
    total_chapters = chapters_result.scalar() or 0

    # Free vs premium chapters
    free_result = await session.execute(
        select(func.count(Chapter.id)).where(Chapter.tier == "free")
    )
    free_chapters = free_result.scalar() or 0

    # Total quiz submissions
    submissions_result = await session.execute(select(func.count(QuizSubmission.id)))
    total_submissions = submissions_result.scalar() or 0

    # Hybrid usage stats
    hybrid_result = await session.execute(
        select(
            func.count(HybridUsage.id),
            func.coalesce(func.sum(HybridUsage.cost_usd), 0),
        )
    )
    hybrid_row = hybrid_result.one()
    total_hybrid_requests = hybrid_row[0] or 0
    total_hybrid_cost = float(hybrid_row[1] or 0)

    # Tier breakdown
    tier_result = await session.execute(
        select(UserProgress.tier, func.count(UserProgress.user_id))
        .group_by(UserProgress.tier)
    )
    tier_breakdown = {row[0]: row[1] for row in tier_result.all()}

    # Completed chapters across all users
    all_progress = await session.execute(select(UserProgress))
    users = all_progress.scalars().all()
    total_completions = sum(len(u.completed_chapters or []) for u in users)

    # Estimated monthly revenue (simple calc)
    premium_count = tier_breakdown.get("premium", 0)
    pro_count = tier_breakdown.get("pro", 0)
    team_count = tier_breakdown.get("team", 0)
    est_revenue = premium_count * 9.99 + pro_count * 19.99 + team_count * 49.99

    return {
        "users": {
            "total": total_users,
            "by_tier": tier_breakdown,
        },
        "content": {
            "total_chapters": total_chapters,
            "free_chapters": free_chapters,
            "premium_chapters": total_chapters - free_chapters,
            "total_completions": total_completions,
        },
        "quizzes": {
            "total_submissions": total_submissions,
        },
        "hybrid_intelligence": {
            "total_requests": total_hybrid_requests,
            "total_cost_usd": round(total_hybrid_cost, 4),
        },
        "revenue": {
            "estimated_monthly_usd": round(est_revenue, 2),
            "premium_subscribers": premium_count,
            "pro_subscribers": pro_count,
            "team_subscribers": team_count,
        },
    }
