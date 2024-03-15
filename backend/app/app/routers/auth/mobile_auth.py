from fastapi import APIRouter

from app.domain.auth.mobile_auth import MobileAuthDomain, UserRegisterModel
from app.models.auth.admin_auth import AuthCheckResponseModel
from app.models.mobile.user import UserResponse
from app.routers.auth import LoginModel, AuthLoginResponseModel


class MobileAuthRoute:

    def __init__(self, domain: MobileAuthDomain):
        self.domain = domain

    @property
    def router(self):
        router = APIRouter(prefix='/mobile/auth', tags=['Mobile Authenticate'])

        @router.post('/login', response_model=AuthLoginResponseModel)
        async def login(login_model: LoginModel):
            return self.domain.login(login_model)

        @router.post('/register', response_model=UserResponse)
        async def register(register_model: UserRegisterModel):
            return self.domain.register(register_model)

        @router.post('/check-email', response_model=AuthCheckResponseModel)
        async def check_email_exist(email: str):
            result = self.domain.check_email(email)
            return AuthCheckResponseModel(result=result)

        @router.post('/check-username', response_model=AuthCheckResponseModel)
        async def check_username_exist(username: str):
            result = self.domain.check_username(username)
            return AuthCheckResponseModel(result=result)

        return router
