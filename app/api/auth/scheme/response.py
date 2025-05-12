from datetime import datetime
from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    access_token_type: str = 'Bearer'
    access_token_expire_time: datetime
    room_id: int = None

class MessageResponse(BaseModel):
    status_code: int | None
    message: str

class ResponseMessage(BaseModel):
    message: str
    run_at: datetime
