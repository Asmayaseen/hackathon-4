from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Chapter(SQLModel, table=True):
    __tablename__ = "chapters"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    r2_key: str = Field(max_length=512, unique=True)  # R2 object key for body text
    order_index: int = Field(unique=True)  # 1-based sequence position
    tier: str = Field(default="free", max_length=10)  # "free" or "premium"
    quiz_id: Optional[int] = Field(default=None, foreign_key="quizzes.id")
    summary: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default=None)
