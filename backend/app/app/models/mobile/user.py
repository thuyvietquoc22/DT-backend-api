from pydantic import Field

from app.models import BaseMongoModel


class UserModelBase(BaseMongoModel):
    username: str = Field(..., example="username")
    email: str = Field(..., example="username@gmail.com")
    fullname: str = Field(..., example="Username")

    class Config:
        from_attributes = True


class UserModelCreate(UserModelBase):
    password: str = Field(..., example="1234qweR@")


class UserResponse(UserModelBase):
    is_active: bool = False
