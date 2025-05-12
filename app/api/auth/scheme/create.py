from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    password: str


class CreateClient(BaseModel):
    code: str
    ip_address: str
    mac_address: str
    username: str
    device_info: str
    desk_number: int

    class Config:
        from_attributes = True
