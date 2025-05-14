from pydantic import BaseModel


class FriendAcceptResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True