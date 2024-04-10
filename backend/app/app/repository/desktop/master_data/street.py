from pymongo.collection import Collection

from app.db.mongo_db import street_collection
from app.decorator import signleton
from app.decorator.parser import parse_as
from app.models.desktop.master_data.street import StreetResponse, StreetUpdate, StreetCreate
from app.repository.base_repository import BaseRepository


@signleton.singleton
class StreetRepository(BaseRepository[StreetResponse, StreetCreate, StreetUpdate]):
    @property
    def collection(self) -> Collection:
        return street_collection

    @property
    def pipeline(self):
        return []

    @parse_as(list[StreetResponse])
    def find_all_by_district(self, district_id):
        pipeline = self.pipeline + [
            {"$match": {"district_code": district_id}}
        ]
        return self.collection.aggregate(pipeline)
