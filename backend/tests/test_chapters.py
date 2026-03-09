import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import patch

from app.models.chapter import Chapter


@pytest.mark.asyncio
async def test_get_chapter_returns_404_for_missing(client: AsyncClient):
    response = await client.get("/chapters/999", headers={"X-User-ID": "test_user"})
    assert response.status_code == 404
    assert response.json()["detail"]["error"] == "not_found"


@pytest.mark.asyncio
async def test_list_chapters_returns_empty_initially(client: AsyncClient):
    response = await client.get("/chapters", headers={"X-User-ID": "test_user"})
    assert response.status_code == 200
    data = response.json()
    assert "chapters" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_previous_chapter_boundary(client: AsyncClient, db_session: AsyncSession):
    # Seed a chapter
    chapter = Chapter(title="Test Ch1", r2_key="chapters/1/test.json", order_index=1, tier="free")
    db_session.add(chapter)
    await db_session.commit()

    with patch("app.r2_client.fetch_chapter_body", return_value={"body": "content", "word_count": 1}):
        with patch("app.services.progress_service.get_or_create_progress") as mock_progress:
            from app.models.user_progress import UserProgress
            mock_progress.return_value = UserProgress(user_id="test_user", tier="free", completed_chapters=[], quiz_scores={})

            response = await client.get("/chapters/1/previous", headers={"X-User-ID": "test_user"})
            assert response.status_code == 200
            data = response.json()
            assert data["is_boundary"] is True
            assert data["boundary_type"] == "first"
            assert data["target"] is None


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
