from typing import Optional

from app.models import BaseMongoModel
from app.models.cms.model import Location
from app.models.desktop.address import Province, District


class BaseCrossRoad(BaseMongoModel):
    name: str
    location: Location
    district_code: int
    province_code: Optional[int] = 0


class CrossRoadCreate(BaseCrossRoad):
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Ngã ba Nguyễn Hữu Thọ - Xô Viết Nghệ Tĩnh",
                "location": {
                    "lat": 16.031314,
                    "lng": 108.208787
                },
                "district_code": 492
            }}
    }


class CrossRoadUpdate(BaseCrossRoad):
    pass


class CrossRoadResponse(BaseCrossRoad):
    province: Optional[Province] = None
    district: Optional[District] = None
