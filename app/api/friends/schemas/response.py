from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str

    class Config:
        from_attributes = True

class FriendRequestResponse(BaseModel):
    request_id: int
    from_user: UserResponse
    to_user: UserResponse
    created_at: datetime

    class Config:
        orm_mode = True

class FriendRequestListResponse(BaseModel):
    count: int
    requests: list[FriendRequestResponse]

    class Config:
        orm_mode = True