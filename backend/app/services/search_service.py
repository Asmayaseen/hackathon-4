from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.chapter import Chapter
from app.models.content_section import ContentSection
from app.schemas.search import ContentSectionResult, SearchResponse


async def _get_accessible_chapter_ids(user_id: str, session: AsyncSession) -> list[int]:
    """Return list of chapter IDs accessible to this user."""
    from app.services.progress_service import get_or_create_progress

    progress = await get_or_create_progress(user_id, session)
    tier = progress.tier

    if tier in ("premium", "pro"):
        result = await session.execute(select(Chapter.id))
        return [row[0] for row in result.all()]

    # Free tier: only chapters 1 through FREE_TIER_MAX_CHAPTER
    result = await session.execute(
        select(Chapter.id).where(Chapter.order_index <= settings.FREE_TIER_MAX_CHAPTER)
    )
    return [row[0] for row in result.all()]


async def search_content(
    query: str,
    user_id: str,
    limit: int,
    session: AsyncSession,
) -> SearchResponse:
    accessible_ids = await _get_accessible_chapter_ids(user_id, session)

    if not accessible_ids:
        return SearchResponse(query=query, total=0, no_results=True, sections=[])

    # PostgreSQL full-text search with ranking
    sql = text("""
        SELECT
            cs.id,
            cs.chapter_id,
            c.title AS chapter_title,
            cs.text,
            ts_rank(cs.text_tsv, plainto_tsquery('english', :query)) AS relevance_score
        FROM content_sections cs
        JOIN chapters c ON c.id = cs.chapter_id
        WHERE
            cs.text_tsv @@ plainto_tsquery('english', :query)
            AND cs.chapter_id = ANY(:chapter_ids)
        ORDER BY relevance_score DESC
        LIMIT :limit
    """)

    result = await session.execute(
        sql,
        {"query": query, "chapter_ids": accessible_ids, "limit": limit},
    )
    rows = result.mappings().all()

    if not rows:
        return SearchResponse(query=query, total=0, no_results=True, sections=[])

    sections = [
        ContentSectionResult(
            id=row["id"],
            chapter_id=row["chapter_id"],
            chapter_title=row["chapter_title"],
            text=row["text"],
            relevance_score=float(row["relevance_score"]),
        )
        for row in rows
    ]

    return SearchResponse(
        query=query,
        total=len(sections),
        no_results=False,
        sections=sections,
    )
