from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


# ── Assessment ────────────────────────────────────────────────────────────────

class AssessmentRequest(BaseModel):
    chapter_id: int
    question: str = Field(max_length=500)
    student_answer: str = Field(min_length=10, max_length=1000)


class AssessmentResponse(BaseModel):
    score: int                      # 0–10
    feedback: str                   # overall feedback
    strengths: list[str]            # what student did well
    improvements: list[str]         # what to work on
    tokens_used: int
    cost_usd: Decimal


# ── Synthesis ─────────────────────────────────────────────────────────────────

class SynthesisRequest(BaseModel):
    chapter_ids: list[int] = Field(min_length=2, max_length=5)
    focus_question: Optional[str] = Field(default=None, max_length=300)


class SynthesisResponse(BaseModel):
    synthesis: str                  # markdown text
    chapters_used: list[str]        # chapter titles included
    tokens_used: int
    cost_usd: Decimal


# ── Usage ─────────────────────────────────────────────────────────────────────

class UsageRecord(BaseModel):
    feature: str
    tokens_input: int
    tokens_output: int
    cost_usd: Decimal
    created_at: str


class UsageSummary(BaseModel):
    user_id: str
    total_requests: int
    total_cost_usd: Decimal
    records: list[UsageRecord]
