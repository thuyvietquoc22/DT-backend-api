from fastapi import APIRouter

from app.routers import MobileTag, BaseRouter
from app.sevices.auth.mobile_auth import MobileAuthService, UserRegisterModel
from app.models.auth.admin_auth import AuthCheckResponseModel
from app.models.mobile.user import UserResponse
from app.routers.auth import LoginModel, AuthLoginResponseModel


class MobileAuthRoute(BaseRouter):

    def __init__(self):
        self.mobile_auth_service = MobileAuthService()

    @property
    def router(self):
        router = APIRouter(prefix='/auth', tags=MobileTag().get("Authenticate"))

        @router.post('/login', response_model=AuthLoginResponseModel)
        async def login(login_model: LoginModel):
            return self.mobile_auth_service.login(login_model)

        @router.post('/register', response_model=UserResponse)
        async def register(register_model: UserRegisterModel):
            return self.mobile_auth_service.register(register_model)

        @router.post('/check-email', response_model=AuthCheckResponseModel)
        async def check_email_exist(email: str):
            result = self.mobile_auth_service.check_email(email)
            return AuthCheckResponseModel(result=result)

        @router.post('/check-username', response_model=AuthCheckResponseModel)
        async def check_username_exist(username: str):
            result = self.mobile_auth_service.check_username(username)
            return AuthCheckResponseModel(result=result)

        return router
