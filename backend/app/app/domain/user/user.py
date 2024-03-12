from pydantic.main import BaseModel


class UserResponse(BaseModel):
    _id: str
    email: str
    fullname: str
    username: str
    is_active: bool
