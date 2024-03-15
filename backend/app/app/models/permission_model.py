from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel

from app.models import BaseMongoModel, PyObjectId
from bson import ObjectId


class SubPermissionModel(BaseMongoModel):
    id: Optional[PyObjectId | ObjectId] = Field(alias="_id", default=ObjectId())
    name: str


class PermissionModel(BaseMongoModel):
    name: str
    sub_permissions: Optional[list[SubPermissionModel]] = None
