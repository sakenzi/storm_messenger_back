from pydantic import BaseModel
from typing import Optional


class MessageCreate(BaseModel):
    recipient_id: int
    text: Optional[str] = None

