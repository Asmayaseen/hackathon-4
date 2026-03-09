from pydantic import BaseModel


class ContentSectionResult(BaseModel):
    id: int
    chapter_id: int
    chapter_title: str
    text: str
    relevance_score: float


class SearchResponse(BaseModel):
    query: str
    total: int
    no_results: bool
    sections: list[ContentSectionResult]
