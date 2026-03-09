from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quiz import Quiz, QuizQuestion
from app.models.quiz_submission import QuizSubmission
from app.schemas.quiz import (
    QuestionResult,
    QuizQuestionResponse,
    QuizResponse,
    QuizResult,
    QuizSubmissionRequest,
)


async def get_quiz_by_chapter(chapter_id: int, session: AsyncSession) -> QuizResponse | None:
    quiz_result = await session.execute(
        select(Quiz).where(Quiz.chapter_id == chapter_id)
    )
    quiz = quiz_result.scalar_one_or_none()

    if quiz is None:
        return QuizResponse(
            quiz_id=0,
            chapter_id=chapter_id,
            title="",
            questions=[],
            total_questions=0,
            no_quiz_available=True,
        )

    questions_result = await session.execute(
        select(QuizQuestion)
        .where(QuizQuestion.quiz_id == quiz.id)
        .order_by(QuizQuestion.position)
    )
    questions = questions_result.scalars().all()

    # CRITICAL: correct_option is NEVER included in the response
    question_responses = [
        QuizQuestionResponse(
            id=q.id,
            position=q.position,
            question_text=q.question_text,
            options=q.options,
        )
        for q in questions
    ]

    return QuizResponse(
        quiz_id=quiz.id,
        chapter_id=chapter_id,
        title=quiz.title,
        questions=question_responses,
        total_questions=len(question_responses),
        no_quiz_available=False,
    )


async def grade_submission(
    quiz_id: int,
    request: QuizSubmissionRequest,
    session: AsyncSession,
) -> QuizResult | None:
    quiz = await session.get(Quiz, quiz_id)
    if quiz is None:
        return None

    questions_result = await session.execute(
        select(QuizQuestion).where(QuizQuestion.quiz_id == quiz_id).order_by(QuizQuestion.position)
    )
    questions = questions_result.scalars().all()

    # Validate all questions are answered
    question_ids = {str(q.id) for q in questions}
    submitted_ids = set(request.answers.keys())
    missing = question_ids - submitted_ids
    if missing:
        return {"error": "validation_error", "missing_questions": sorted(int(x) for x in missing)}

    # Grade each question
    score = 0
    results = []
    for q in questions:
        submitted = request.answers.get(str(q.id), "")
        passed = submitted.upper() == q.correct_option.upper()
        if passed:
            score += 1
        results.append(
            QuestionResult(
                question_id=q.id,
                submitted_answer=submitted,
                correct_answer=q.correct_option,
                passed=passed,
                explanation=q.explanation,
            )
        )

    max_score = len(questions)
    percentage = round((score / max_score) * 100, 1) if max_score > 0 else 0.0
    passed_quiz = percentage >= 60.0

    # Save submission record
    submission = QuizSubmission(
        user_id=request.user_id,
        quiz_id=quiz_id,
        submitted_at=datetime.utcnow(),
        answers=request.answers,
        score=score,
        max_score=max_score,
        passed=passed_quiz,
    )
    session.add(submission)
    await session.commit()
    await session.refresh(submission)

    # Update progress with quiz score
    from app.services.progress_service import update_quiz_score
    await update_quiz_score(request.user_id, quiz.chapter_id, score, session)

    return QuizResult(
        submission_id=submission.id,
        quiz_id=quiz_id,
        user_id=request.user_id,
        score=score,
        max_score=max_score,
        percentage=percentage,
        passed=passed_quiz,
        results=results,
    )
