from bson import ObjectId

from app.models import BaseMongoModel, PyObjectId


class BaseAccount(BaseMongoModel):
    email: str
    fullname: str
    is_active: bool


class AccountCreate(BaseAccount):
    username: str
    fullname: str
    email: str
    password: str
    role_id: ObjectId
    first_login: bool


class AccountUpdate(BaseAccount):
    password: str


class AccountResponse(BaseAccount):
    username: str
    role_id: PyObjectId
    first_login: bool
    role_name: str


class AccountModel(AccountResponse):
    password: str
