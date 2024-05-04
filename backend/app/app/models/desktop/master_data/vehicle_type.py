from app.models import BaseMongoModel


class VehicleTypeBase(BaseMongoModel):
    type: str  # Unique
    description: str
    size: float
    name: str


class VehicleTypeCreate(VehicleTypeBase):
    pass


class VehicleTypeUpdate(VehicleTypeBase):
    pass


class VehicleTypeResponse(VehicleTypeBase):
    pass
