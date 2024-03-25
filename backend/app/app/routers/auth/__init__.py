from pydantic import BaseModel, Field

from app.models.admin.permission import PermissionResponse


class AuthLoginResponseModel(BaseModel):
    access_token: str = Field(..., examples=[''])
    refresh_token: str = Field(..., examples=[''])
    permissions: list[PermissionResponse] = Field(..., examples=[''])
    token_type: str = Field("bearer", examples=['bearer'])
    first_login: bool = Field(..., examples=[True])


class LoginModel(BaseModel):
    username: str = Field(..., examples=['username'])
    password: str = Field(..., examples=['password'])
