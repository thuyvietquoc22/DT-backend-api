from datetime import datetime
from typing import Literal, Optional

from billiard.five import values
from pydantic import BaseModel

from app.models.cms.model import Location
from app.models.desktop.master_data.passage_capacity_status import PassageCapacityStatus
from app.models.desktop.master_data.street import StreetResponse


class Bounce(BaseModel):
    min_lat: float
    max_lat: float
    min_lng: float
    max_lng: float
    # Template
    model_config = {
        "json_schema_extra": {
            "example": {
                "min_lat": 16.034968,
                "max_lat": 108.205672,
                "min_lng": 16.029452,
                "max_lng": 108.226168
            }}
    }

    @property
    def center(self):
        return {
            "lat": (self.min_lat + self.max_lat) / 2,
            "lng": (self.min_lng + self.max_lng) / 2
        }


class PassageCapacityRequest:
    bounce: Bounce


class PassageCapacityValue(BaseModel):
    camera_id: str
    location: Location
    camera_direction: Literal[-1, 1]
    passage_capacity_current: int
    passage_capacity_ratio: float
    passage_capacity_status: Optional[PassageCapacityStatus] = None
    street: StreetResponse
    at: Optional[datetime]


class PassageCapacityResponse(BaseModel):
    # bounce_requested: Bounce
    # at: datetime
    values: list[PassageCapacityValue]
