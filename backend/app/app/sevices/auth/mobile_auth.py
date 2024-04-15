from app.core.jwt import create_access_token, create_refresh_token
from app.core.password_encoder import verify_password, hash_password
from app.decorator import signleton
from app.decorator.parser import parse_as
from app.exceptions.authenticate_exception import AuthenticateException
from app.exceptions.param_invalid_exception import ParamInvalidException
from app.models.auth.mobile_auth import UserRegisterModel
from app.models.mobile.user import UserModelCreate
from app.repository.mobile.user import UserRepository
from app.routers.auth import LoginModel, AuthLoginResponseModel


@signleton.singleton
class MobileAuthService:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def check_email(self, email: str) -> bool:
        exist_user = self.user_repo.find_by_email(email)
        return exist_user is not None

    def check_username(self, username: str) -> bool:
        exist_user = self.user_repo.find_by_username(username)
        return exist_user is not None

    def login(self, model: LoginModel):
        user = self.user_repo.find_by_username(model.username)
        if user is None:
            raise AuthenticateException("Can't find mobile with this username")

        if not verify_password(model.password, user.get("password")):
            raise AuthenticateException("Password is incorrect")

        access_token = create_access_token(user.get("username"))
        refresh_token = create_refresh_token(user.get("username"))
        token_type = "bearer"

        return AuthLoginResponseModel(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=token_type
        )

    @parse_as(response_type=UserModelCreate)
    def register(self, register: UserRegisterModel):

        exist_user = self.user_repo.find_by_username(register.username)
        if exist_user is not None:
            raise ParamInvalidException("Tên người dùng đã tồn tại")

        exist_user = self.user_repo.find_by_email(register.email)
        if exist_user is not None:
            raise ParamInvalidException("Email đã tồn tại")

        user = UserModelCreate(**register.dict())
        user.password = hash_password(user.password)

        return self.user_repo.create(user)


mobile_auth_service = MobileAuthService(UserRepository())
