from typing import Optional

from pydantic import Field, BaseModel

from app.models import BaseMongoModel, PyObjectId
from app.models.cms.model import Location


class VMSSignBase(BaseMongoModel):
    """Các thuộc tính cở bản của biển báo."""
    id_model: PyObjectId
    vms_sign_code: str
    resource: str
    ip_address: str = Field(pattern=r'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b')
    username: str
    password: str


class VMSSignCreate(VMSSignBase):
    model_config = {
        "json_schema_extra": {
            "example": {
                "id_model": "660699f497fbc609d2cdf2f6",
                "vms_sign_code": "VMS_SIGN_NHT_XVNT",
                "resource": "Sở giao thông vận tải",
                "ip_address": "0.0.0.0",
                "username": "admin",
                "password": "admin"
            }}
    }


class VMSSignUpdate(BaseModel):
    vms_sign_code: Optional[str] = None
    resource: Optional[str] = None
    ip_address: Optional[str] = Field(pattern=r'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b', default=None)
    username: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "vms_sign_code": "VMS_SIGN_NHT_XVNT",
                "resource": "Sở giao thông vận tải",
                "ip_address": "0.0.0.0",
                "username": "admin"
            }
        }
    }


class VMSSignResponse(VMSSignBase):
    location: Location
