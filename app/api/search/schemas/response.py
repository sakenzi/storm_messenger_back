from pydantic import BaseModel
from datetime import datetime


class UsersResponse(BaseModel):
    id: int
    username: str
    full_name: str
    online: bool
    last_visit: datetime

    class Config:
        from_attributes = True