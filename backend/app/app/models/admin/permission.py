from typing import Optional

from app.models import BaseMongoModel


class SubPermissionModel(BaseMongoModel):
    keyname: str
    name: str


class PermissionModel(BaseMongoModel):
    name: str
    keyname: str
    sub_permissions: Optional[list[SubPermissionModel]] = None


class PermissionResponse(PermissionModel):
    pass
