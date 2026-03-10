from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel


class HybridUsage(SQLModel, table=True):
    __tablename__ = "hybrid_usage"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(max_length=255)
    feature: str = Field(max_length=50)       # 'assess' or 'synthesize'
    chapter_ids: Optional[str] = Field(default=None)  # JSON: "[1,2,3]"
    tokens_input: int = Field(default=0)
    tokens_output: int = Field(default=0)
    cost_usd: Decimal = Field(default=Decimal("0"))
    created_at: Optional[datetime] = Field(default=None)
