from datetime import date, datetime
from typing import Optional

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy import Integer
from sqlmodel import Field, SQLModel


class UserProgress(SQLModel, table=True):
    __tablename__ = "user_progress"

    user_id: str = Field(max_length=128, primary_key=True)
    tier: str = Field(default="free", max_length=10)
    completed_chapters: list[int] = Field(
        default_factory=list,
        sa_column=Column(ARRAY(Integer), nullable=False, server_default="{}"),
    )
    quiz_scores: dict = Field(
        default_factory=dict,
        sa_column=Column(JSONB, nullable=False, server_default="{}"),
    )
    current_streak: int = Field(default=0)
    longest_streak: int = Field(default=0)
    last_activity_date: Optional[date] = Field(default=None)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)
