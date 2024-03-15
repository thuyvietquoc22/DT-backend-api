from typing import Optional

from bson import ObjectId
from pydantic import Field

from app.models import BaseMongoModel, PyObjectId


class SubPermissionModel(BaseMongoModel):
    id: Optional[PyObjectId | ObjectId] = Field(alias="_id", default=ObjectId())
    name: str


class PermissionModel(BaseMongoModel):
    name: str
    sub_permissions: Optional[list[SubPermissionModel]] = None
