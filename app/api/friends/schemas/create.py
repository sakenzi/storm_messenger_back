from pydantic import BaseModel
from typing import Optional


class FriendRequest(BaseModel):
    to_user_id: int