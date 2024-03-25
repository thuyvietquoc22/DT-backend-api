from typing import Optional

from bson import ObjectId
from pydantic import Field, BaseModel

from app.models import BaseMongoModel, PyObjectId


class SimplePermission(BaseMongoModel):
    name: str
    keyname: str


class PermissionBase(SimplePermission):
    sub_permissions: Optional[list[SimplePermission]] = None


class PermissionCreate(PermissionBase):
    pass


class PermissionResponse(PermissionBase):
    pass
