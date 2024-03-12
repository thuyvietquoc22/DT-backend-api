from fastapi import APIRouter

from app.domain.auth.auth import UserLoginModel, UserRegisterModel, AuthCheckResponseModel
from app.services.mobile_auth import mobile_auth_service


class MobileAuthRoute:

    @property
    def router(self):
        router = APIRouter(prefix='/mobile/auth', tags=['Mobile Authenticate'])

        @router.post('/login')
        async def login(login_model: UserLoginModel):
            mobile_auth_service.login(login_model)

        @router.post('/register')
        async def register(register_model: UserRegisterModel):
            mobile_auth_service.register(register_model)

        @router.post('/check-email')
        async def check_email_exist(email: str):
            result = mobile_auth_service.check_email(email)
            return AuthCheckResponseModel(registered=result)

        @router.post('/check-username')
        async def check_username_exist(username: str):
            result = mobile_auth_service.check_username(username)
            return AuthCheckResponseModel(registered=result)

        return router


mobile_auth_router: MobileAuthRoute = MobileAuthRoute()
