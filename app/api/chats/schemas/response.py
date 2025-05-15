from pydantic import BaseModel


class MessageResponse(BaseModel):
    sender_id: int
    recipient_id: int
    text: str

    class Config:
        from_attributes = True