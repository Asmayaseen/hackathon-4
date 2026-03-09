from typing import Optional
from pydantic import BaseModel


class ChapterMeta(BaseModel):
    id: int
    title: str
    order_index: int
    tier: str
    has_quiz: bool
    summary: Optional[str] = None


class ChapterDetail(ChapterMeta):
    body: str
    word_count: int
    total_chapters: int


class ChapterNavigation(BaseModel):
    current_chapter_id: int
    target: Optional[ChapterMeta] = None
    is_boundary: bool
    boundary_type: Optional[str] = None  # "first" or "last"


class ChapterListResponse(BaseModel):
    chapters: list[ChapterMeta]
    total: int
