from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.db.mongo_db import user_collection, user_collection
from app.domain.auth.auth import UserRegisterModel, UserLoginModel, AuthLoginResponseModel
from app.exceptions.authenticate_exception import AuthenticateException
from app.exceptions.param_invalid_exception import ParamInvalidException
from app.models.user_model import UserModel


class MobileAuthService:

    @staticmethod
    def login(model: UserLoginModel):
        user = user_collection.find_one({"username": model.email})
        if user is None:
            raise AuthenticateException("Can't find user with this username")

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

    @staticmethod
    def register(register: UserRegisterModel):

        exist_user = user_collection.find_one({"username": register.username})
        if exist_user is not None:
            raise ParamInvalidException("Tên người dùng đã tồn tại")

        exist_user = user_collection.find_one({"email": register.email})
        if exist_user is not None:
            raise ParamInvalidException("Email đã tồn tại")

        user: UserModel = UserModel(
            **register.dict(),
        )
        user.password = get_password_hash(user.password)

        user_collection.insert_one(user.dict())

    @staticmethod
    def check_email(email: str):
        exist_user = user_collection.find_one({"email": email})
        return exist_user is not None

    @staticmethod
    def check_username(username: str):
        exist_user = user_collection.find_one({"username": username})
        return exist_user is not None


mobile_auth_service = MobileAuthService()
