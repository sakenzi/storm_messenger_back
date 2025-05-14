from pydantic import BaseModel, Field
from typing import Optional


class UserRegister(BaseModel):
    username: Optional[str] = Field("", max_length=50)
    full_name: str = Field(..., max_length=100)
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    username: str = Field(..., max_length=50)
    password: str = Field(..., min_length=8)

