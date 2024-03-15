from pydantic import BaseModel
from pydantic.v1 import Field


class AuthLoginResponseModel(BaseModel):
    access_token: str = Field(..., example='')
    refresh_token: str = Field(..., example='')
    token_type: str = Field("bearer", example='')


class LoginModel(BaseModel):
    username: str = Field(..., example='username')
    password: str = Field(..., example='password')
