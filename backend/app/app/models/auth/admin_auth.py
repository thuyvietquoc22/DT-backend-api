from typing import Optional

from pydantic import BaseModel, Field


class AccountLogin(BaseModel):
    email: str = Field(..., example=['email'])
    password: str = Field(..., example=['password'])


class AccountRegisterModel(BaseModel):
    username: str = Field(..., example=['username'])
    fullname: Optional[str] = Field(..., example=['Nguyen Van Anh'])
    email: str = Field(..., example=['account@gmail.com'])
    password: str = Field(..., example=['password'])
    role_id: str = Field(..., example=['admin'])


class AuthTokenModel(BaseModel):
    token: Optional[str] = Field(..., example=[''])


class AuthCheckResponseModel(BaseModel):
    result: bool = Field(..., example=[False])


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None


# First Login
class FirstLoginModel(BaseModel):
    password: str = Field(..., example=['password'])
    access_token: str = Field(..., example=[''])
