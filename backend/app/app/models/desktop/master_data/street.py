from typing import Literal, Optional

from pydantic import BaseModel

from app.models import BaseMongoModel
from app.models.cms.model import Location


class StreetBase(BaseMongoModel):
    start_location: Location
    end_location: Location
    length: float
    width: float
    max_speed: int
    type: Literal["one-way", "two-way"]
    passage_capacity: int
    district_code: list[int]


class StreetCreate(StreetBase):
    pass


class StreetUpdate(BaseModel):
    start_location: Optional[Location] = None
    end_location: Optional[Location] = None
    length: Optional[float] = None
    width: Optional[float] = None
    max_speed: Optional[int] = None
    type: Optional[Literal["one-way", "two-way"]] = None
    passage_capacity: Optional[int] = None
    district_code: list[int] = None


class StreetResponse(StreetBase):
    pass
