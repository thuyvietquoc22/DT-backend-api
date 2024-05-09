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
    protocol: str
    endpoint: Optional[str] = None
    port: int


class VMSSignCreate(VMSSignBase):
    pass


class VMSSignUpdate(BaseModel):
    vms_sign_code: Optional[str] = None
    resource: Optional[str] = None
    ip_address: Optional[str] = Field(pattern=r'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b', default=None)
    username: Optional[str] = None
    protocol: Optional[str] = None
    endpoint: Optional[str] = None
    port: Optional[int] = None


class VMSSignResponse(VMSSignBase):
    location: Location
