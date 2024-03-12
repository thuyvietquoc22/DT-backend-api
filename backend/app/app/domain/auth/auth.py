from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class UserLoginModel(BaseModel):
    username: str = Field(..., example='username')
    password: str = Field(..., example='password')


class UserRegisterModel(BaseModel):
    username: str = Field(..., example='username')
    email: str = Field(..., example='email')
    password: str = Field(..., example='password')
    phone: Optional[str] = Field(..., example='phone')


class AuthTokenModel(BaseModel):
    token: Optional[str] = Field(..., example='')


class AuthLoginResponseModel(BaseModel):
    access_token: Optional[str] = Field(..., example='')
    refresh_token: Optional[str] = Field(..., example='')
    token_type: Optional[str] = Field(..., example='')


class AuthCheckEmailResponseModel(BaseModel):
    is_email_registered: bool = Field(..., example=True)


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
