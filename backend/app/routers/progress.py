from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas.progress import UserProgressResponse
from app.services import progress_service

router = APIRouter(prefix="/progress", tags=["Progress"])


class ChapterCompleteRequest(BaseModel):
    completed: bool = True


@router.get("/{user_id}", response_model=UserProgressResponse)
async def get_progress(
    user_id: str,
    session: AsyncSession = Depends(get_session),
) -> UserProgressResponse:
    return await progress_service.get_progress(user_id, session)


@router.put("/{user_id}/chapters/{chapter_id}", response_model=UserProgressResponse)
async def mark_chapter_complete(
    user_id: str,
    chapter_id: int,
    request: ChapterCompleteRequest,
    session: AsyncSession = Depends(get_session),
) -> UserProgressResponse:
    if not request.completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "invalid_request", "message": "completed must be true"},
        )
    return await progress_service.mark_chapter_complete(user_id, chapter_id, session)
