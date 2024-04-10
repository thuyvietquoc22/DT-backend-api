from typing import Optional

from pydantic import BaseModel

from app.models import BaseMongoModel, PyObjectId
from app.models.cms.model import Location
from app.models.desktop.master_data.address import Province, District


class BaseCrossRoad(BaseMongoModel):
    name: str
    location: Location
    district_code: int
    province_code: Optional[int] = 0
    street_ids: list[PyObjectId] = []


class CrossRoadCreate(BaseCrossRoad):
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Ngã ba Nguyễn Hữu Thọ - Xô Viết Nghệ Tĩnh",
                "location": {
                    "lat": 16.031314,
                    "lng": 108.208787
                },
                "district_code": 492,
                "street_id": ["<id_street>", "<id_street>"]
            }}
    }


class CrossRoadUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[Location] = None
    district_code: Optional[int] = None
    province_code: Optional[int] = None
    street_ids: Optional[list[PyObjectId]] = None

class CrossRoadResponse(BaseCrossRoad):
    province: Optional[Province] = None
    district: Optional[District] = None
