from datetime import date, timedelta

import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch

from app.schemas.progress import UserProgressResponse


def _mock_progress(
    user_id="test_user",
    completed=[],
    streak=0,
    last_date=None,
    tier="free",
) -> UserProgressResponse:
    return UserProgressResponse(
        user_id=user_id,
        tier=tier,
        completed_chapters=completed,
        quiz_scores={},
        current_streak=streak,
        longest_streak=streak,
        last_activity_date=last_date,
        course_completion_pct=len(completed) * 20.0,
        total_quiz_score=0,
    )


@pytest.mark.asyncio
async def test_get_progress_unknown_user_returns_zero_state(client: AsyncClient):
    with patch("app.services.progress_service.get_progress", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = _mock_progress("brand_new_user")
        response = await client.get("/progress/brand_new_user")
        assert response.status_code == 200
        data = response.json()
        assert data["current_streak"] == 0
        assert data["completed_chapters"] == []
        assert data["course_completion_pct"] == 0.0


@pytest.mark.asyncio
async def test_mark_chapter_complete_increments_streak(client: AsyncClient):
    with patch("app.services.progress_service.mark_chapter_complete", new_callable=AsyncMock) as mock_mark:
        mock_mark.return_value = _mock_progress(completed=[1], streak=1, last_date=date.today())
        response = await client.put(
            "/progress/test_user/chapters/1",
            json={"completed": True},
        )
        assert response.status_code == 200
        data = response.json()
        assert 1 in data["completed_chapters"]
        assert data["current_streak"] == 1


@pytest.mark.asyncio
async def test_missed_day_resets_streak():
    """Unit test for streak logic directly."""
    from app.models.user_progress import UserProgress
    from app.services.progress_service import _calculate_streak

    yesterday = date.today() - timedelta(days=1)
    progress_consecutive = UserProgress(
        user_id="u1", tier="free", completed_chapters=[],
        quiz_scores={}, current_streak=5, longest_streak=5,
        last_activity_date=yesterday,
    )
    assert _calculate_streak(progress_consecutive) == 6

    two_days_ago = date.today() - timedelta(days=2)
    progress_broken = UserProgress(
        user_id="u1", tier="free", completed_chapters=[],
        quiz_scores={}, current_streak=5, longest_streak=5,
        last_activity_date=two_days_ago,
    )
    assert _calculate_streak(progress_broken) == 1

    progress_today = UserProgress(
        user_id="u1", tier="free", completed_chapters=[],
        quiz_scores={}, current_streak=3, longest_streak=3,
        last_activity_date=date.today(),
    )
    assert _calculate_streak(progress_today) == 3  # No change
