from typing import Optional

from pydantic import BaseModel

from app.models import BaseMongoModel


class VehicleTypeBase(BaseMongoModel):
    type: str  # Unique
    description: str
    size: float
    name: str


class VehicleTypeCreate(VehicleTypeBase):
    pass


class VehicleTypeUpdate(BaseModel):
    type: Optional[str] = None
    description: Optional[str] = None
    size: Optional[float] = None
    name: Optional[str] = None


class VehicleTypeResponse(VehicleTypeBase):
    pass
