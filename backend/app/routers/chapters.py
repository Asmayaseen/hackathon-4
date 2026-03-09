from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas.chapter import ChapterDetail, ChapterListResponse, ChapterNavigation
from app.services import access_service, content_service

router = APIRouter(prefix="/chapters", tags=["Chapters"])


@router.get("", response_model=ChapterListResponse)
async def list_chapters(
    x_user_id: str = Header(..., alias="X-User-ID"),
    session: AsyncSession = Depends(get_session),
) -> ChapterListResponse:
    return await content_service.get_chapter_list(session)


@router.get("/{chapter_id}", response_model=ChapterDetail)
async def get_chapter(
    chapter_id: int,
    x_user_id: str = Header(..., alias="X-User-ID"),
    session: AsyncSession = Depends(get_session),
) -> ChapterDetail:
    access = await access_service.check_access(x_user_id, f"chapter_{chapter_id}", session)
    if not access.access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "access": False,
                "reason": access.reason,
                "upgrade_url": access.upgrade_url,
                "message": "This chapter requires a Premium subscription.",
            },
        )

    chapter = await content_service.get_chapter(chapter_id, session)
    if chapter is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": f"Chapter with id={chapter_id} does not exist."},
        )
    return chapter


@router.get("/{chapter_id}/next", response_model=ChapterNavigation)
async def get_next_chapter(
    chapter_id: int,
    x_user_id: str = Header(..., alias="X-User-ID"),
    session: AsyncSession = Depends(get_session),
) -> ChapterNavigation:
    nav = await content_service.get_next_chapter(chapter_id, session)
    if nav is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": f"Chapter with id={chapter_id} does not exist."},
        )
    return nav


@router.get("/{chapter_id}/previous", response_model=ChapterNavigation)
async def get_previous_chapter(
    chapter_id: int,
    x_user_id: str = Header(..., alias="X-User-ID"),
    session: AsyncSession = Depends(get_session),
) -> ChapterNavigation:
    nav = await content_service.get_previous_chapter(chapter_id, session)
    if nav is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": f"Chapter with id={chapter_id} does not exist."},
        )
    return nav
