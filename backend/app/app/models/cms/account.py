from typing import Optional

from bson import ObjectId
from pydantic import BaseModel

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


class AccountUpdate(BaseModel):
    username: Optional[str] = None
    fullname: Optional[str] = None
    role_id: Optional[PyObjectId] = None


class AccountResponse(BaseAccount):
    username: str
    role_id: PyObjectId
    first_login: bool
    role_name: Optional[str] = None


class AccountModel(AccountResponse):
    password: str
    role_name: Optional[str] = None
