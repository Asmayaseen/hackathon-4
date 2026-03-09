from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.schemas.access import AccessCheck


async def check_access(user_id: str, resource: str, session: AsyncSession) -> AccessCheck:
    """
    Check if user_id has access to the given resource.
    resource format: "chapter_N" or "quiz_N"
    Free tier: chapters 1–FREE_TIER_MAX_CHAPTER only.
    Premium/Pro: all chapters.
    """
    # Get user tier (lazy import to avoid circular deps)
    from app.services.progress_service import get_or_create_progress

    progress = await get_or_create_progress(user_id, session)
    tier = progress.tier

    # Parse resource
    chapter_num = _extract_chapter_num(resource)
    if chapter_num is None:
        # Unknown resource type — allow by default
        return AccessCheck(access=True)

    if tier in ("premium", "pro"):
        return AccessCheck(access=True)

    # Free tier: only chapters 1 through FREE_TIER_MAX_CHAPTER
    if chapter_num <= settings.FREE_TIER_MAX_CHAPTER:
        return AccessCheck(access=True)

    return AccessCheck(
        access=False,
        reason="premium_required",
        upgrade_url=settings.UPGRADE_URL,
    )


def _extract_chapter_num(resource: str) -> int | None:
    """Parse 'chapter_N' or 'quiz_N' → chapter number, else None."""
    for prefix in ("chapter_", "quiz_"):
        if resource.startswith(prefix):
            try:
                return int(resource[len(prefix):])
            except ValueError:
                return None
    return None
