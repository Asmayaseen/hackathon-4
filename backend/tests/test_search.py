import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch

from app.schemas.search import ContentSectionResult, SearchResponse


@pytest.mark.asyncio
async def test_search_returns_no_results_for_nonsense(client: AsyncClient):
    with patch("app.services.search_service.search_content", new_callable=AsyncMock) as mock_search:
        mock_search.return_value = SearchResponse(
            query="banana smoothie recipe",
            total=0,
            no_results=True,
            sections=[],
        )
        response = await client.get(
            "/search?q=banana+smoothie+recipe",
            headers={"X-User-ID": "test_user"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["no_results"] is True
        assert data["sections"] == []
        assert data["total"] == 0


@pytest.mark.asyncio
async def test_search_returns_sections_for_known_query(client: AsyncClient):
    mock_section = ContentSectionResult(
        id=1,
        chapter_id=3,
        chapter_title="Model Context Protocol (MCP)",
        text="MCP (Model Context Protocol) is an open standard...",
        relevance_score=0.87,
    )
    with patch("app.services.search_service.search_content", new_callable=AsyncMock) as mock_search:
        mock_search.return_value = SearchResponse(
            query="What is MCP",
            total=1,
            no_results=False,
            sections=[mock_section],
        )
        response = await client.get(
            "/search?q=What+is+MCP",
            headers={"X-User-ID": "test_user"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["no_results"] is False
        assert len(data["sections"]) == 1
        assert data["sections"][0]["chapter_id"] == 3


@pytest.mark.asyncio
async def test_search_requires_query_param(client: AsyncClient):
    response = await client.get("/search", headers={"X-User-ID": "test_user"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_search_requires_user_id_header(client: AsyncClient):
    response = await client.get("/search?q=MCP")
    assert response.status_code == 422
