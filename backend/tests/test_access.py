import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch

from app.schemas.access import AccessCheck


@pytest.mark.asyncio
async def test_free_user_blocked_at_chapter_4(client: AsyncClient):
    with patch("app.services.access_service.check_access", new_callable=AsyncMock) as mock_access:
        mock_access.return_value = AccessCheck(
            access=False,
            reason="premium_required",
            upgrade_url="https://example.com/upgrade",
        )
        response = await client.get(
            "/access/check?user_id=free_user&resource=chapter_4"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["access"] is False
        assert data["reason"] == "premium_required"
        assert "upgrade_url" in data


@pytest.mark.asyncio
async def test_free_user_passes_for_chapter_1(client: AsyncClient):
    with patch("app.services.access_service.check_access", new_callable=AsyncMock) as mock_access:
        mock_access.return_value = AccessCheck(access=True)
        response = await client.get(
            "/access/check?user_id=free_user&resource=chapter_1"
        )
        assert response.status_code == 200
        assert response.json()["access"] is True


@pytest.mark.asyncio
async def test_chapter_4_returns_403_for_free_user(client: AsyncClient):
    with patch("app.services.access_service.check_access", new_callable=AsyncMock) as mock_access:
        mock_access.return_value = AccessCheck(
            access=False,
            reason="premium_required",
            upgrade_url="https://example.com/upgrade",
        )
        response = await client.get("/chapters/4", headers={"X-User-ID": "free_user"})
        assert response.status_code == 403
        detail = response.json()["detail"]
        assert detail["access"] is False
        assert detail["reason"] == "premium_required"


@pytest.mark.asyncio
async def test_access_check_unit():
    """Unit test access_service directly."""
    from app.services.access_service import _extract_chapter_num

    assert _extract_chapter_num("chapter_4") == 4
    assert _extract_chapter_num("chapter_1") == 1
    assert _extract_chapter_num("quiz_3") == 3
    assert _extract_chapter_num("unknown") is None
