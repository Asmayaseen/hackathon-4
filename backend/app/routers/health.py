from fastapi import APIRouter
from app.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check() -> dict:
    return {"status": "ok", "version": settings.APP_VERSION}
