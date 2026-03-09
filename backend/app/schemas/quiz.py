from typing import Optional
from pydantic import BaseModel


class QuizQuestionResponse(BaseModel):
    """Question schema — correct_option is intentionally EXCLUDED."""
    id: int
    position: int
    question_text: str
    options: dict[str, str]  # {"A": "...", "B": "...", "C": "...", "D": "..."}


class QuizResponse(BaseModel):
    quiz_id: int
    chapter_id: int
    title: str
    questions: list[QuizQuestionResponse]
    total_questions: int
    no_quiz_available: bool


class QuizSubmissionRequest(BaseModel):
    user_id: str
    answers: dict[str, str]  # {question_id (str) -> "A"/"B"/"C"/"D"}


class QuestionResult(BaseModel):
    question_id: int
    submitted_answer: str
    correct_answer: str
    passed: bool
    explanation: Optional[str] = None


class QuizResult(BaseModel):
    submission_id: int
    quiz_id: int
    user_id: str
    score: int
    max_score: int
    percentage: float
    passed: bool
    results: list[QuestionResult]
