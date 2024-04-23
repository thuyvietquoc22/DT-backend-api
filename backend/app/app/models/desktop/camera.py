from typing import Optional, Literal

from bson import ObjectId
from pydantic import Field, BaseModel, field_serializer

from app.models import BaseMongoModel, PyObjectId
from app.models.cms.model import Location
from app.models.desktop.master_data.street import StreetResponse
from app.models.desktop.traffic_data import TrafficDataResponse


class BaseCamera(BaseMongoModel):
    """Các thuộc tính cở bản của camera."""
    id_model: PyObjectId
    camera_code: str
    resource: str
    ip_address: str = Field(pattern=r'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b')
    username: str
    password: str
    direction: Literal[-1, 1]
    street_id: PyObjectId


class CameraCreate(BaseCamera):
    @field_serializer("id_model", "street_id")
    def serializer_id_model(self, value: PyObjectId) -> ObjectId:
        return ObjectId(value)


class CameraUpdate(BaseModel):
    # id_model: Optional[PyObjectId] = None
    camera_code: Optional[str] = None
    resource: Optional[str] = None
    ip_address: Optional[str] = Field(pattern=r'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b', default=None)
    username: Optional[str] = None
    direction: Optional[Literal[-1, 1]]
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


class CameraTrafficDataResponse(CameraResponse):
    live_passage_capacity: list[TrafficDataResponse]
    street: StreetResponse
