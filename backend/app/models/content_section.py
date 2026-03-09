from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ContentSection(SQLModel, table=True):
    __tablename__ = "content_sections"

    id: Optional[int] = Field(default=None, primary_key=True)
    chapter_id: int = Field(foreign_key="chapters.id")
    section_index: int
    text: str
    # text_tsv is a GENERATED column (computed by PostgreSQL) — not mapped here
    created_at: Optional[datetime] = Field(default=None)
