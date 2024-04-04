from typing import Optional

from pydantic import Field, BaseModel

from app.models import BaseMongoModel, PyObjectId
from app.models.cms.model import Location


class BaseCamera(BaseMongoModel):
    """Các thuộc tính cở bản của camera."""
    id_model: PyObjectId
    camera_code: str
    resource: str
    ip_address: str = Field(pattern=r'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b')
    username: str


class CameraControl(BaseModel):
    angle_x: int
    angle_y: int
    zoom: float
    fov: float
    focal_length: float


class CameraCreate(BaseCamera):
    password: str
    model_config = {
        "json_schema_extra": {
            "example": {
                "model_id": "660699f497fbc609d2cdf2f6",
                "camera_code": "CAMERA_NHT_XVNT",
                "resource": "Sở giao thông vận tải",
                "ip_address": "0.0.0.0",
                "username": "admin",
                "password": "admin"
            }}
    }


class CameraUpdate(BaseModel):
    # id_model: Optional[PyObjectId] = None
    camera_code: Optional[str] = None
    resource: Optional[str] = None
    ip_address: Optional[str] = Field(pattern=r'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b', default=None)
    username: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "camera_code": "CAMERA_NHT_XVNT",
                "resource": "Sở giao thông vận tải",
                "ip_address": "0.0.0.0",
                "username": "admin"
            }
        }
    }


class CameraResponse(BaseCamera):
    location: Location
