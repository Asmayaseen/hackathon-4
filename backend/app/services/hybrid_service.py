"""
Phase 2 Hybrid Intelligence Service
Uses Claude Sonnet for:
  1. LLM-Graded Assessments  — evaluates free-form written answers
  2. Cross-Chapter Synthesis  — connects concepts across chapters

ISOLATION RULE: This file is the ONLY place in backend/app/ where LLM calls are made.
All Phase 1 routes must remain zero-LLM.
"""
import json
from decimal import Decimal

from anthropic import Anthropic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.chapter import Chapter
from app.models.content_section import ContentSection
from app.models.hybrid_usage import HybridUsage
from app.schemas.hybrid import AssessmentResponse, SynthesisResponse

# Claude Sonnet pricing (per million tokens)
_INPUT_COST_PER_M = Decimal("3.00")   # $3.00 / 1M input tokens
_OUTPUT_COST_PER_M = Decimal("15.00") # $15.00 / 1M output tokens

MODEL = "claude-sonnet-4-6"


def _get_client() -> Anthropic:
    return Anthropic(api_key=settings.ANTHROPIC_API_KEY)


def _calc_cost(input_tokens: int, output_tokens: int) -> Decimal:
    return (
        Decimal(input_tokens) / Decimal(1_000_000) * _INPUT_COST_PER_M +
        Decimal(output_tokens) / Decimal(1_000_000) * _OUTPUT_COST_PER_M
    ).quantize(Decimal("0.000001"))


async def _log_usage(
    session: AsyncSession,
    user_id: str,
    feature: str,
    chapter_ids: list[int],
    input_tokens: int,
    output_tokens: int,
    cost_usd: Decimal,
) -> None:
    record = HybridUsage(
        user_id=user_id,
        feature=feature,
        chapter_ids=json.dumps(chapter_ids),
        tokens_input=input_tokens,
        tokens_output=output_tokens,
        cost_usd=cost_usd,
    )
    session.add(record)
    await session.commit()


async def assess_answer(
    chapter_id: int,
    question: str,
    student_answer: str,
    user_id: str,
    session: AsyncSession,
) -> AssessmentResponse:
    """Grade a free-form written answer using Claude Sonnet."""

    # Fetch chapter content as grounding material
    chapter = await session.get(Chapter, chapter_id)
    chapter_body = chapter.body or "" if chapter else ""
    chapter_title = chapter.title if chapter else f"Chapter {chapter_id}"

    prompt = f"""You are an expert educational assessor for the course "AI Agent Development".

CHAPTER CONTENT (use this as grounding):
Title: {chapter_title}
{chapter_body[:3000]}

ASSESSMENT TASK:
Question asked to student: {question}
Student's answer: {student_answer}

Evaluate the student's answer on a scale of 0-10 based on:
- Accuracy and correctness
- Depth of understanding
- Clarity of explanation
- Use of relevant concepts

Respond in this exact JSON format:
{{
  "score": <integer 0-10>,
  "feedback": "<overall 2-3 sentence feedback>",
  "strengths": ["<strength 1>", "<strength 2>"],
  "improvements": ["<improvement 1>", "<improvement 2>"]
}}

Be encouraging but honest. Only evaluate based on the chapter content provided."""

    client = _get_client()
    message = client.messages.create(
        model=MODEL,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    # Extract JSON from response
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()

    data = json.loads(raw)
    input_tokens = message.usage.input_tokens
    output_tokens = message.usage.output_tokens
    cost = _calc_cost(input_tokens, output_tokens)

    await _log_usage(session, user_id, "assess", [chapter_id], input_tokens, output_tokens, cost)

    return AssessmentResponse(
        score=int(data["score"]),
        feedback=data["feedback"],
        strengths=data.get("strengths", []),
        improvements=data.get("improvements", []),
        tokens_used=input_tokens + output_tokens,
        cost_usd=cost,
    )


async def synthesize_chapters(
    chapter_ids: list[int],
    focus_question: str | None,
    user_id: str,
    session: AsyncSession,
) -> SynthesisResponse:
    """Generate a cross-chapter synthesis using Claude Sonnet."""

    # Fetch content for each chapter
    chapters_content = []
    chapter_titles = []
    for cid in chapter_ids:
        chapter = await session.get(Chapter, cid)
        if not chapter:
            continue
        chapter_titles.append(chapter.title)
        body = chapter.body or ""
        chapters_content.append(f"## {chapter.title}\n{body[:1500]}")

    combined = "\n\n".join(chapters_content)
    focus = f"\nFocus question: {focus_question}" if focus_question else ""

    prompt = f"""You are an expert educational synthesizer for "AI Agent Development" course.

COURSE CONTENT FROM MULTIPLE CHAPTERS:
{combined}
{focus}

Create a cross-chapter synthesis that:
1. Identifies how concepts from different chapters connect and build on each other
2. Shows the "big picture" of how these topics fit together
3. Highlights key relationships and dependencies between concepts
4. Uses clear markdown formatting with headings

Write a comprehensive synthesis (400-600 words) that helps students see the complete picture.
Start with a brief overview, then explain the connections, then summarize the key insight."""

    client = _get_client()
    message = client.messages.create(
        model=MODEL,
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
    )

    synthesis_text = message.content[0].text.strip()
    input_tokens = message.usage.input_tokens
    output_tokens = message.usage.output_tokens
    cost = _calc_cost(input_tokens, output_tokens)

    await _log_usage(session, user_id, "synthesize", chapter_ids, input_tokens, output_tokens, cost)

    return SynthesisResponse(
        synthesis=synthesis_text,
        chapters_used=chapter_titles,
        tokens_used=input_tokens + output_tokens,
        cost_usd=cost,
    )
