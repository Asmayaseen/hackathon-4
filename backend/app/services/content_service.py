from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chapter import Chapter
from app.r2_client import fetch_chapter_body
from app.schemas.chapter import ChapterDetail, ChapterListResponse, ChapterMeta, ChapterNavigation


def _to_meta(chapter: Chapter, has_quiz: bool) -> ChapterMeta:
    return ChapterMeta(
        id=chapter.id,
        title=chapter.title,
        order_index=chapter.order_index,
        tier=chapter.tier,
        has_quiz=has_quiz,
        summary=chapter.summary,
    )


async def get_chapter_list(session: AsyncSession) -> ChapterListResponse:
    result = await session.execute(select(Chapter).order_by(Chapter.order_index))
    chapters = result.scalars().all()
    metas = [_to_meta(c, has_quiz=c.quiz_id is not None) for c in chapters]
    return ChapterListResponse(chapters=metas, total=len(metas))


async def get_chapter(chapter_id: int, session: AsyncSession) -> ChapterDetail:
    chapter = await session.get(Chapter, chapter_id)
    if not chapter:
        return None

    # Try R2 first; fall back to DB body column
    r2_data = fetch_chapter_body(chapter.r2_key)
    body = r2_data.get("body") or chapter.body or ""
    word_count = r2_data.get("word_count") or chapter.word_count or 0

    # Count total chapters for navigation context
    count_result = await session.execute(select(Chapter))
    total = len(count_result.scalars().all())

    return ChapterDetail(
        id=chapter.id,
        title=chapter.title,
        order_index=chapter.order_index,
        tier=chapter.tier,
        has_quiz=chapter.quiz_id is not None,
        summary=chapter.summary,
        body=body,
        word_count=word_count,
        total_chapters=total,
    )


async def get_next_chapter(chapter_id: int, session: AsyncSession) -> ChapterNavigation:
    chapter = await session.get(Chapter, chapter_id)
    if not chapter:
        return None

    next_result = await session.execute(
        select(Chapter)
        .where(Chapter.order_index > chapter.order_index)
        .order_by(Chapter.order_index)
        .limit(1)
    )
    next_chapter = next_result.scalar_one_or_none()

    if next_chapter is None:
        return ChapterNavigation(
            current_chapter_id=chapter_id,
            target=None,
            is_boundary=True,
            boundary_type="last",
        )

    return ChapterNavigation(
        current_chapter_id=chapter_id,
        target=_to_meta(next_chapter, has_quiz=next_chapter.quiz_id is not None),
        is_boundary=False,
    )


async def get_previous_chapter(chapter_id: int, session: AsyncSession) -> ChapterNavigation:
    chapter = await session.get(Chapter, chapter_id)
    if not chapter:
        return None

    prev_result = await session.execute(
        select(Chapter)
        .where(Chapter.order_index < chapter.order_index)
        .order_by(Chapter.order_index.desc())
        .limit(1)
    )
    prev_chapter = prev_result.scalar_one_or_none()

    if prev_chapter is None:
        return ChapterNavigation(
            current_chapter_id=chapter_id,
            target=None,
            is_boundary=True,
            boundary_type="first",
        )

    return ChapterNavigation(
        current_chapter_id=chapter_id,
        target=_to_meta(prev_chapter, has_quiz=prev_chapter.quiz_id is not None),
        is_boundary=False,
    )
