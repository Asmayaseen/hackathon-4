from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas.quiz import QuizResponse, QuizResult, QuizSubmissionRequest
from app.services import access_service, quiz_service

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])


@router.get("/chapter/{chapter_id}", response_model=QuizResponse)
async def get_quiz_by_chapter(
    chapter_id: int,
    x_user_id: str = Header(..., alias="X-User-ID"),
    session: AsyncSession = Depends(get_session),
) -> QuizResponse:
    access = await access_service.check_access(x_user_id, f"quiz_{chapter_id}", session)
    if not access.access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "access": False,
                "reason": access.reason,
                "upgrade_url": access.upgrade_url,
                "message": "This quiz requires a Premium subscription.",
            },
        )

    result = await quiz_service.get_quiz_by_chapter(chapter_id, session)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": f"Chapter {chapter_id} not found."},
        )
    return result


@router.post("/{quiz_id}/submit", response_model=QuizResult)
async def submit_quiz(
    quiz_id: int,
    request: QuizSubmissionRequest,
    session: AsyncSession = Depends(get_session),
) -> QuizResult:
    result = await quiz_service.grade_submission(quiz_id, request, session)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": f"Quiz {quiz_id} not found."},
        )

    if isinstance(result, dict) and result.get("error") == "validation_error":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "validation_error",
                "message": f"Missing answers for questions: {result['missing_questions']}",
                "missing_questions": result["missing_questions"],
            },
        )

    return result
