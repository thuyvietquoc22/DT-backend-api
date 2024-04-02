from typing import Literal, Optional

from bson import ObjectId
from pydantic import BaseModel

from app.models import BaseMongoModel, PyObjectId
from app.models.admin.assets import AssetsResponse


class Location(BaseModel):
    lat: float
    lng: float

    def __eq__(self, other):
        return self.lat == other.lat and self.lng == other.lng

    def to_array(self):
        return [self.lat, self.lng]


ModelType = Literal["2D", "3D"]


class ModelBase(BaseMongoModel):
    name: str
    location: Location
    scale: float
    bearing: float
    elevation: float


class ModelCreate(ModelBase):
    asset_id: str


class ModelUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[ModelType] = None
    location: Optional[Location] = None
    scale: Optional[float] = None
    bearing: Optional[float] = None
    elevation: Optional[float] = None
    asset_ids: Optional[str] = None


class ModelResponse(ModelBase):
    asset: AssetsResponse | None = None
