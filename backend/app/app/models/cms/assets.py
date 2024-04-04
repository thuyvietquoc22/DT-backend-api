from typing import Optional

from bson import ObjectId

from app.models import BaseMongoModel


class GroupAssets(BaseMongoModel):
    name: str  # Tên của group asset
    keyname: str  # Keyname của group asset


class AssetsBase(BaseMongoModel):
    name: str  # Tên của asset không liên qua đến public id của cloudinary có thể trùng lặp
    object_3d: str  # URL của object 3d
    texture: str  # URL của texture
    image: str  # URL của image
    public_id: str  # Public id của asset trên cloudinary


class AssetsCreate(AssetsBase):
    group_id: ObjectId


class AssetsUpdate(AssetsBase):
    group_id: Optional[str] = None


class AssetsResponse(AssetsBase):
    group: GroupAssets
