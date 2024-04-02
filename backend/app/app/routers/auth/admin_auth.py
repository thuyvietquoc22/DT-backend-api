from fastapi import APIRouter

from app.domain.auth.admin_auth import AccountLogin, AuthLoginResponseModel, AccountRegisterModel, AdminAuthDomain
from app.models.auth.admin_auth import AuthTokenModel, AuthCheckResponseModel, FirstLoginModel
from app.models.pagination_model import Pageable


class AdminAuthRouter:

    def __init__(self, domain: AdminAuthDomain):
        self.domain = domain

    @property
    def router(self):
        api_router = APIRouter(prefix='/cms/auth', tags=['Auth'])

        @api_router.get("/accounts")
        async def get_accounts(limit: int = 10, page: int = 1):
            pageable = Pageable.of(limit=limit, page=page)
            result = self.domain.get_accounts(pageable)
            return result

        @api_router.post('/validate')
        async def validate(request: AuthTokenModel):
            return self.domain.validate_token(request.token)

        @api_router.post('/login', response_model=AuthLoginResponseModel)
        async def login(user_login_model: AccountLogin):
            return self.domain.login(user_login_model)

        @api_router.post('/change-password-first-login')
        async def change_password(request: FirstLoginModel):
            self.domain.change_password_first_login(request)
            return {"message": "Change password success"}

        @api_router.post('/create-system-account')
        async def register(user_register: AccountRegisterModel):
            self.domain.register(user_register)
            return {"message": "Create account success"}

        @api_router.post('/check-email', response_model=AuthCheckResponseModel)
        async def check_exist_email(email: str):
            result = self.domain.check_exist_email(email)
            return AuthCheckResponseModel(result=result)

        return api_router
