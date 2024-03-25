from app.models import BaseMongoModel, PyObjectId


class BaseAccount(BaseMongoModel):
    email: str
    fullname: str
    is_active: bool


class AccountCreate(BaseAccount):
    username: str
    password: str


class AccountUpdate(BaseAccount):
    password: str


class AccountResponse(BaseAccount):
    username: str
    role_id: PyObjectId
    first_login: bool


class AccountModel(AccountResponse):
    password: str
