from pydantic.main import BaseModel


class UserModel(BaseModel):
    _id: int
    username: str
    password: str
    email: str
    fullname: str
    is_active: bool = False

    class Config:
        orm_mode = True
