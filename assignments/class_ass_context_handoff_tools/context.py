from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

class UserInfo(BaseModel):
    uid: str = Field(default_factory=lambda: str(uuid4()))
    name: Optional[str] = None
    text: Optional[str] = None
    reply: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))