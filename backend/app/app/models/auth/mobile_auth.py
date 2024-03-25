from typing import Optional

from pydantic import BaseModel, Field


class UserRegisterModel(BaseModel):
    username: str = Field(..., example=['username'])
    email: str = Field(..., example=['moblie@gmail.com'])
    password: str = Field(..., example=['password'])
    fullname: Optional[str] = Field(..., example=['Nguyen Van Anh'])
