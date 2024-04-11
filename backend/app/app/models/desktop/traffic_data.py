from datetime import datetime
from typing import Literal, Optional

from bson import ObjectId
from pydantic import BaseModel, field_serializer

from app.models import BaseMongoModel, PyObjectId


class VehicleCount(BaseModel):
    vehicle_type: Literal["CAR", "MOTORBIKE", "TRUCK", "BUS", "OTHERS"]
    count: int


class TrafficDataBase(BaseMongoModel):
    time: Optional[datetime] = None
    vehicle_count: list[VehicleCount]
    camera_id: PyObjectId

    @field_serializer("camera_id", )
    def serializer_camera_id(self, value: PyObjectId) -> ObjectId:
        return ObjectId(value)


class TrafficDataCreate(TrafficDataBase):
    model_config = {
        "json_schema_extra": {
            "example": {
                "time": "2021-08-30T07:00:00",
                "vehicle_count": [{
                    "vehicle_type": "CAR",
                    "count": 10
                }],
                "camera_id": "660699f497fbc609d2cdf2f6"
            }
        }
    }


class TrafficDataResponse(TrafficDataBase):
    @field_serializer("camera_id", )
    def serializer_camera_id(self, value: PyObjectId) -> str:
        return str(value)
