from typing import Optional
from pydantic import BaseModel


class AccessCheck(BaseModel):
    access: bool
    reason: Optional[str] = None
    upgrade_url: Optional[str] = None


class AccessDenied(BaseModel):
    access: bool = False
    reason: str
    upgrade_url: str
    message: str
