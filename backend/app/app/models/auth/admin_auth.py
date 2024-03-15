from typing import Optional

from pydantic import BaseModel
from pydantic.v1 import Field


class AccountLogin(BaseModel):
    email: str = Field(..., example='email')
    password: str = Field(..., example='password')


class AccountRegisterModel(BaseModel):
    username: str = Field(..., example='username')
    email: str = Field(..., example='moblie@gmail.com')
    password: str = Field(..., example='password')
    fullname: Optional[str] = Field(..., example='Nguyen Van Anh')


class AuthTokenModel(BaseModel):
    token: Optional[str] = Field(..., example='')


class AuthCheckResponseModel(BaseModel):
    result: bool = Field(..., example=False)


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
