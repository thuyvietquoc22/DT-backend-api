from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi_cognito import CognitoToken

from app.domain.auth.auth import (
    AuthCheckEmailResponseModel,
    AuthLoginSNSModel
)

from app.domain.auth.auth import AuthDomain, UserLoginModel, AuthLoginResponseModel, UserSNSModel


class AuthRouter:
    def __init__(self, auth_domain: AuthDomain) -> None:
        self.auth_domain = auth_domain

    @property
    def router(self):
        api_router = APIRouter(prefix='/auth', tags=['Auth'])


       
        return api_router
