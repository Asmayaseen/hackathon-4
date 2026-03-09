from datetime import datetime
from typing import Optional

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class QuizSubmission(SQLModel, table=True):
    __tablename__ = "quiz_submissions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(max_length=128)
    quiz_id: int = Field(foreign_key="quizzes.id")
    submitted_at: Optional[datetime] = Field(default=None)
    answers: dict = Field(sa_column=Column(JSONB, nullable=False))
    score: int
    max_score: int
    passed: bool
