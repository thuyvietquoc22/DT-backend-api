from fastapi import APIRouter

from app.domain.auth.admin_auth import AccountLogin, AuthLoginResponseModel, AccountRegisterModel, AdminAuthDomain
from app.models.auth.admin_auth import AuthTokenModel, AuthCheckResponseModel


class AdminAuthRouter:

    def __init__(self, domain: AdminAuthDomain):
        self.domain = domain

    @property
    def router(self):
        api_router = APIRouter(prefix='/auth', tags=['Auth'])

        @api_router.post('/validate')
        async def validate(request: AuthTokenModel):
            return self.domain.validate_token(request.token)

        @api_router.post('/login', response_model=AuthLoginResponseModel)
        async def login(user_login_model: AccountLogin):
            return self.domain.login(user_login_model)

        @api_router.post('/register')
        async def register(user_register: AccountRegisterModel):
            return self.domain.register(user_register)

        @api_router.post('/check-email', response_model=AuthCheckResponseModel)
        async def check_exist_email(email: str):
            result = self.domain.check_exist_email(email)
            return AuthCheckResponseModel(result=result)

        return api_router


