from app.core.security import verify_password, get_password_hash, create_refresh_token, create_access_token, \
    extract_jwt_token
from app.db.mongo_db import account_collection
from app.domain.auth.auth import UserLoginModel, AuthLoginResponseModel, UserRegisterModel, AuthTokenModel
from app.exceptions.authenticate_exception import AuthenticateException
from app.exceptions.param_invalid_exception import ParamInvalidException


class AuthService:

    @staticmethod
    def validate_token(token: str):
        return extract_jwt_token(token)

    @staticmethod
    def login(user_login_model: UserLoginModel) -> AuthLoginResponseModel:

        user = account_collection.find_one({"email": user_login_model.email})
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

    @staticmethod
    def register(user_register: UserRegisterModel):

        exist_user = account_collection.find_one({"username": user_register.username})

        if exist_user is not None:
            raise ParamInvalidException("Username already exist")

        user_register.password = get_password_hash(user_register.password)
        account_collection.insert_one(user_register.dict())

        return True

    @staticmethod
    def check_exist_email(email: str):
        exist_user = account_collection.find_one({"email": email})
        return exist_user is not None


auth_service = AuthService()
