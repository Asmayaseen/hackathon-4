from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas.access import AccessCheck
from app.services import access_service

router = APIRouter(tags=["Access"])


@router.get("/access/check", response_model=AccessCheck)
async def check_access(
    user_id: str = Query(..., description="Student identifier"),
    resource: str = Query(..., description="Resource identifier, e.g. 'chapter_4' or 'quiz_4'"),
    session: AsyncSession = Depends(get_session),
) -> AccessCheck:
    return await access_service.check_access(user_id, resource, session)
