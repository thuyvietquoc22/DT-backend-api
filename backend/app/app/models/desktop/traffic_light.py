from typing import Optional

from pydantic import Field, BaseModel

from app.models import PyObjectId, BaseMongoModel
from app.models.cms.model import Location


class BaseTrafficLight(BaseMongoModel):
    """Các thuộc tính cở bản của Đèn tín hiệu."""
    id_model: PyObjectId
    traffic_light_code: str
    resource: str
    ip_address: str = Field(pattern=r'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b')
    username: str
    password: str


class TrafficLightCreate(BaseTrafficLight):
    model_config = {
        "json_schema_extra": {
            "example": {
                "id_model": "660699f497fbc609d2cdf2f6",
                "traffic_light_code": "TRAFFIC_LIGHT_NHT_XVNT",
                "resource": "Sở giao thông vận tải",
                "ip_address": "0.0.0.0",
                "username": "admin",
                "password": "admin"
            }}
    }


class TrafficLightUpdate(BaseModel):
    # id_model: Optional[PyObjectId] = None
    camera_code: Optional[str] = None
    resource: Optional[str] = None
    ip_address: Optional[str] = Field(pattern=r'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b', default=None)
    username: Optional[str] = None


class TrafficLightResponse(BaseTrafficLight):
    location: Location


class TrafficLightControl(BaseModel):
    pass
