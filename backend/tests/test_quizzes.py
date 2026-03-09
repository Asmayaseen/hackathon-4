import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch

from app.schemas.quiz import (
    QuestionResult,
    QuizQuestionResponse,
    QuizResponse,
    QuizResult,
)


@pytest.mark.asyncio
async def test_quiz_questions_do_not_contain_correct_option(client: AsyncClient):
    mock_quiz = QuizResponse(
        quiz_id=1,
        chapter_id=1,
        title="Chapter 1 Quiz",
        questions=[
            QuizQuestionResponse(
                id=1,
                position=1,
                question_text="What are the four key properties of an AI agent?",
                options={"A": "opt1", "B": "Perception, reasoning, action, memory", "C": "opt3", "D": "opt4"},
            )
        ],
        total_questions=1,
        no_quiz_available=False,
    )
    with patch("app.services.quiz_service.get_quiz_by_chapter", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_quiz
        with patch("app.services.access_service.check_access", new_callable=AsyncMock) as mock_access:
            from app.schemas.access import AccessCheck
            mock_access.return_value = AccessCheck(access=True)

            response = await client.get("/quizzes/chapter/1", headers={"X-User-ID": "test_user"})
            assert response.status_code == 200
            data = response.json()
            # CRITICAL: correct_option must never appear in response
            response_str = str(data)
            assert "correct_option" not in response_str
            assert len(data["questions"]) == 1


@pytest.mark.asyncio
async def test_quiz_grading_returns_score(client: AsyncClient):
    mock_result = QuizResult(
        submission_id=1,
        quiz_id=1,
        user_id="test_user",
        score=5,
        max_score=5,
        percentage=100.0,
        passed=True,
        results=[
            QuestionResult(
                question_id=i,
                submitted_answer="B",
                correct_answer="B",
                passed=True,
                explanation="Correct!",
            )
            for i in range(1, 6)
        ],
    )
    with patch("app.services.quiz_service.grade_submission", new_callable=AsyncMock) as mock_grade:
        mock_grade.return_value = mock_result

        response = await client.post(
            "/quizzes/1/submit",
            json={
                "user_id": "test_user",
                "answers": {"1": "B", "2": "B", "3": "B", "4": "B", "5": "B"},
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["score"] == 5
        assert data["passed"] is True
        assert data["percentage"] == 100.0


@pytest.mark.asyncio
async def test_incomplete_submission_returns_400(client: AsyncClient):
    with patch("app.services.quiz_service.grade_submission", new_callable=AsyncMock) as mock_grade:
        mock_grade.return_value = {
            "error": "validation_error",
            "missing_questions": [3, 4, 5],
        }

        response = await client.post(
            "/quizzes/1/submit",
            json={"user_id": "test_user", "answers": {"1": "A", "2": "B"}},
        )
        assert response.status_code == 400
        data = response.json()
        assert data["detail"]["error"] == "validation_error"
