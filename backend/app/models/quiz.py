from datetime import datetime
from typing import Optional

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class Quiz(SQLModel, table=True):
    __tablename__ = "quizzes"

    id: Optional[int] = Field(default=None, primary_key=True)
    chapter_id: int = Field(foreign_key="chapters.id", unique=True)
    title: str = Field(max_length=255)
    created_at: Optional[datetime] = Field(default=None)


class QuizQuestion(SQLModel, table=True):
    __tablename__ = "quiz_questions"

    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_id: int = Field(foreign_key="quizzes.id")
    question_text: str
    options: dict = Field(sa_column=Column(JSONB, nullable=False))
    correct_option: str = Field(max_length=1)  # A, B, C, or D — NEVER in API responses
    explanation: Optional[str] = Field(default=None)
    position: int
    created_at: Optional[datetime] = Field(default=None)
