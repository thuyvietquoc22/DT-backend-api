from fastapi import APIRouter

from app.domain.auth.auth import UserLoginModel, AuthLoginResponseModel, UserRegisterModel, AuthTokenModel
from app.services.auth import auth_service


class AuthRouter:

    @property
    def router(self):
        api_router = APIRouter(prefix='/auth', tags=['Auth'])

        @api_router.post('/validate')
        async def validate(request: AuthTokenModel):
            return auth_service.validate_token(request.token)

        @api_router.post('/login', response_model=AuthLoginResponseModel)
        async def login(user_login_model: UserLoginModel):
            return auth_service.login(user_login_model)

        @api_router.post('/register')
        async def register(user_register: UserRegisterModel):
            return auth_service.register(user_register)

        return api_router
