from datetime import date
from typing import Optional
from pydantic import BaseModel


class UserProgressResponse(BaseModel):
    user_id: str
    tier: str
    completed_chapters: list[int]
    quiz_scores: dict[str, int]
    current_streak: int
    longest_streak: int
    last_activity_date: Optional[date] = None
    course_completion_pct: float
    total_quiz_score: int
