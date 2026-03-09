from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas.search import SearchResponse
from app.services import search_service

router = APIRouter(tags=["Search"])


@router.get("/search", response_model=SearchResponse)
async def search_content(
    q: str = Query(..., min_length=2, max_length=500, description="Student's question or search query"),
    limit: int = Query(default=5, ge=1, le=10),
    x_user_id: str = Header(..., alias="X-User-ID"),
    session: AsyncSession = Depends(get_session),
) -> SearchResponse:
    return await search_service.search_content(q, x_user_id, limit, session)
