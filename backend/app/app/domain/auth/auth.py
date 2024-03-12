from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class UserLoginModel(BaseModel):
    email: str = Field(..., example='email')
    password: str = Field(..., example='password')


class UserRegisterModel(BaseModel):
    username: str = Field(..., example='username')
    email: str = Field(..., example='user@gmail.com')
    password: str = Field(..., example='password')
    phone: Optional[str] = Field(..., example='0123456789')
    fullname: Optional[str] = Field(..., example='Nguyen Van Anh')


class AuthTokenModel(BaseModel):
    token: Optional[str] = Field(..., example='')


class AuthLoginResponseModel(BaseModel):
    access_token: Optional[str] = Field(..., example='')
    refresh_token: Optional[str] = Field(..., example='')
    token_type: Optional[str] = Field(..., example='')


class AuthCheckResponseModel(BaseModel):
    registered: bool = Field(..., example=True)


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
