from app.core.security import verify_password, get_password_hash, create_refresh_token, create_access_token
from app.db.mongo_db import users_collection
from app.domain.auth.auth import UserLoginModel, AuthLoginResponseModel, UserRegisterModel


class AuthService:
    @staticmethod
    def login(user_login_model: UserLoginModel) -> AuthLoginResponseModel:

        user = users_collection.find_one({"username": user_login_model.username})
        if user is None:
            raise ValueError("Invalid username")

        if not verify_password(user_login_model.password, user.get("password")):
            raise ValueError("Invalid password")

        access_token = create_access_token(user.get("username"), demo_attribute="demo")
        refresh_token = create_refresh_token(user.get("username"), demo_attribute="demo")
        token_type = "bearer"

        return AuthLoginResponseModel(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=token_type
        )

    @staticmethod
    def register(user_register: UserRegisterModel):

        exist_user = users_collection.find_one({"username": user_register.username})

        if exist_user is not None:
            raise ValueError("Username already exist")

        user_register.password = get_password_hash(user_register.password)
        users_collection.insert_one(user_register.dict())

        return True


auth_service = AuthService()
