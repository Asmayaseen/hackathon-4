from datetime import date, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_progress import UserProgress
from app.schemas.progress import UserProgressResponse


async def get_or_create_progress(user_id: str, session: AsyncSession) -> UserProgress:
    """Get existing progress or auto-create a zero-state record for new users."""
    progress = await session.get(UserProgress, user_id)
    if progress is None:
        progress = UserProgress(
            user_id=user_id,
            tier="free",
            completed_chapters=[],
            quiz_scores={},
            current_streak=0,
            longest_streak=0,
            last_activity_date=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        session.add(progress)
        await session.commit()
        await session.refresh(progress)
    return progress


def _calculate_streak(progress: UserProgress) -> int:
    """Recalculate streak based on last_activity_date and today (UTC)."""
    today = date.today()

    if progress.last_activity_date is None:
        return 1

    delta = (today - progress.last_activity_date).days

    if delta == 0:
        return progress.current_streak  # Already logged today
    elif delta == 1:
        return progress.current_streak + 1  # Consecutive day
    else:
        return 1  # Streak broken — reset to 1


async def mark_chapter_complete(
    user_id: str,
    chapter_id: int,
    session: AsyncSession,
) -> UserProgressResponse:
    progress = await get_or_create_progress(user_id, session)

    if chapter_id not in progress.completed_chapters:
        progress.completed_chapters = progress.completed_chapters + [chapter_id]

    new_streak = _calculate_streak(progress)
    progress.current_streak = new_streak
    progress.longest_streak = max(progress.longest_streak, new_streak)
    progress.last_activity_date = date.today()
    progress.updated_at = datetime.utcnow()

    session.add(progress)
    await session.commit()
    await session.refresh(progress)

    return _to_response(progress)


async def update_quiz_score(
    user_id: str,
    chapter_id: int,
    score: int,
    session: AsyncSession,
) -> None:
    """Update quiz score and streak after a quiz submission."""
    progress = await get_or_create_progress(user_id, session)

    scores = dict(progress.quiz_scores)
    scores[str(chapter_id)] = score
    progress.quiz_scores = scores

    new_streak = _calculate_streak(progress)
    progress.current_streak = new_streak
    progress.longest_streak = max(progress.longest_streak, new_streak)
    progress.last_activity_date = date.today()
    progress.updated_at = datetime.utcnow()

    session.add(progress)
    await session.commit()


async def get_progress(user_id: str, session: AsyncSession) -> UserProgressResponse:
    progress = await get_or_create_progress(user_id, session)
    return _to_response(progress)


def _to_response(progress: UserProgress) -> UserProgressResponse:
    # Compute total chapters dynamically — hardcode 5 for Phase 1
    # (can be made dynamic by querying DB in Phase 2)
    total_chapters = 5
    completion_pct = round(len(progress.completed_chapters) / total_chapters * 100, 1)
    total_score = sum(int(v) for v in progress.quiz_scores.values())

    return UserProgressResponse(
        user_id=progress.user_id,
        tier=progress.tier,
        completed_chapters=progress.completed_chapters or [],
        quiz_scores={str(k): int(v) for k, v in (progress.quiz_scores or {}).items()},
        current_streak=progress.current_streak,
        longest_streak=progress.longest_streak,
        last_activity_date=progress.last_activity_date,
        course_completion_pct=completion_pct,
        total_quiz_score=total_score,
    )
