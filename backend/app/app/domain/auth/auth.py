import random
from fastapi import HTTPException
from typing import Optional

from pydantic import Field
from pydantic import BaseModel
from starlette.background import BackgroundTasks

from app.third_party.cognito_aws import (
    initiate_auth_with_username_password,
    create_user,
    is_email_registered,
    update_password,
    get_user_by_email,
    revoke_access_token,
    get_email_by_user_id,
    refresh_access_token
)
from app.third_party.ses_aws import ses_send_mail
from app.utils.redis import RedisService


from app.utils.logging import logger
from uuid import uuid4
from datetime import datetime
from botocore.exceptions import ClientError
from app.core.config import settings


class UserLoginModel(BaseModel):
    username: str = Field(..., example='sangnd')
    password: str = Field(..., example='Abc!234')
    device_token: Optional[dict] = None

class UserSNSModel(BaseModel):
    code: str = Field(..., example='AQBOKlXZcEZVUONlt9pfNlDRgodU6YQsqDXotpwMyiR....')
    sns_type: int = Field(..., example=1)
    user_id: Optional[str] = None


class AuthLoginSNSModel(BaseModel):
    code: str = Field(..., example='AQBOKlXZcEZVUONlt9pfNlDRgodU6YQsqDXotpwMyiR....')
    sns_type: int = Field(..., example=1)
    display_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    description: Optional[str] = None
    account_type: Optional[str] = None
    gender: Optional[int] = None
    boxing_watch_history: Optional[str] = None
    favorite_tags: Optional[list] = []
    favorite_other: Optional[str] = None
    white_list_categories: Optional[list] = []
    back_list_categories: Optional[list] = []


class AuthLoginResponseModel(BaseModel):
    access_token: Optional[str] = Field(..., example='')
    refresh_token: Optional[str] = Field(..., example='')
    token_type: Optional[str] = Field(..., example='')


class AuthCheckEmailResponseModel(BaseModel):
    is_email_registered: bool = Field(..., example=True)


class TokenPayload(BaseModel):
    sub: Optional[str] = None


class AuthDomain:
    def __init__(
            self,
    ) -> None:
        self.__repository = True

   