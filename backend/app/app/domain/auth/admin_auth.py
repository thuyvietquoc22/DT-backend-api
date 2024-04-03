from bson import ObjectId

from app.core import jwt
from app.core.jwt import create_refresh_token, create_access_token, extract_jwt_token
from app.core.password_encoder import verify_password, hash_password
from app.domain.admin.permission import permission_domain
from app.domain.admin.role import role_domain
from app.exceptions.authenticate_exception import AuthenticateException
from app.exceptions.param_invalid_exception import ParamInvalidException
from app.models.admin.account import AccountCreate, AccountResponse, AccountModel
from app.models.admin.role import RoleResponse
from app.models.auth.admin_auth import AccountLogin, AccountRegisterModel, FirstLoginModel
from app.models.pagination_model import Pageable
from app.repository.admin.account import AccountRepository
from app.routers.auth import AuthLoginResponseModel


class AdminAuthDomain:

    def __init__(self, account_repo: AccountRepository):
        self.account_repo = account_repo

    @staticmethod
    def validate_token(token: str):
        return extract_jwt_token(token)

    def login(self, user_login_model: AccountLogin) -> AuthLoginResponseModel:

        user: AccountModel = self.account_repo.find_by_email(user_login_model.email)

        if user is None:
            raise AuthenticateException("Email này chưa được đăng ký")

        if not verify_password(user_login_model.password, user.password):
            raise AuthenticateException("Mật khẩu không chính xác")

        permissions: RoleResponse = role_domain.get_permission_by_role_id(user.role_id)

        access_token = create_access_token(user.email)
        refresh_token = create_refresh_token(user.email)

        return AuthLoginResponseModel(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            permissions=permissions.permissions,
            first_login=user.first_login
        )

    def register(self, account_register: AccountRegisterModel):

        exist_account = self.check_exist_email(account_register.email)

        if exist_account:
            raise ParamInvalidException("Email này đã được sử dụng")

        account_register.password = hash_password(account_register.password)

        account = AccountCreate(
            username=account_register.username,
            fullname=account_register.fullname,
            email=account_register.email,
            password=account_register.password,
            role_id=ObjectId(account_register.role_id),
            is_active=True,
            first_login=True
        )

        return self.account_repo.create(account)

    def check_exist_email(self, email: str):
        exist_user = self.account_repo.find_by_email(email)
        return exist_user is not None

    def change_password_first_login(self, request: FirstLoginModel):
        decode = jwt.extract_jwt_token(request.access_token)
        user = self.account_repo.find_by_email(decode['username'])
        if user is None:
            raise AuthenticateException("Không tìm thấy tài khoản")

        if not user.first_login:
            raise AuthenticateException("Tài khoản đã thay đổi mật khẩu")

        hashed_password = hash_password(request.password)
        user.first_login = False
        self.account_repo.update_first_login(_id=user.id, hash_password=hashed_password)

    def get_accounts(self, pageable: Pageable):
        result = self.account_repo.find_all(pageable)
        return result

    def delete_account(self, _id):
        result = self.account_repo.delete(_id)
        return result


admin_auth_domain = AdminAuthDomain(AccountRepository())
