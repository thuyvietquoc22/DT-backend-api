from app.core.jwt import create_refresh_token, create_access_token, extract_jwt_token
from app.core.password_encoder import verify_password, hash_password
from app.exceptions.authenticate_exception import AuthenticateException
from app.exceptions.param_invalid_exception import ParamInvalidException
from app.models.admin.account import AccountCreate
from app.models.auth.admin_auth import AccountLogin, AccountRegisterModel
from app.repository.admin.account import AccountRepository
from app.routers.auth import AuthLoginResponseModel


class AdminAuthDomain:

    def __init__(self, account_repo: AccountRepository):
        self.account_repo = account_repo

    @staticmethod
    def validate_token(token: str):
        return extract_jwt_token(token)

    def login(self, user_login_model: AccountLogin) -> AuthLoginResponseModel:

        user = self.account_repo.find_by_email(user_login_model.email)
        if user is None:
            raise AuthenticateException("Email này chưa được đăng ký")

        if not verify_password(user_login_model.password, user.get("password")):
            raise AuthenticateException("Mật khẩu không chính xác")

        access_token = create_access_token(user.get("email"))
        refresh_token = create_refresh_token(user.get("email"))

        return AuthLoginResponseModel(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

    def register(self, account_register: AccountRegisterModel):

        exist_account = self.check_exist_email(account_register.email)

        if exist_account is not None:
            raise ParamInvalidException("Username already exist")

        account_register.password = hash_password(account_register.password)

        account = AccountCreate(
            **account_register.dict(),
            is_active=False
        )

        return self.account_repo.create(account)

    def check_exist_email(self, email: str):
        exist_user = self.account_repo.find_by_email(email)
        return exist_user is not None


admin_auth_domain = AdminAuthDomain(AccountRepository())
