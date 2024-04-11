from pymongo.collection import Collection

from app.db.mongo_db import passage_capacity_status_collection
from app.decorator import signleton
from app.decorator.parser import parse_as
from app.models.desktop.master_data.passage_capacity_status import PassageCapacityStatus
from app.repository.base_repository import BaseRepository


@signleton.singleton
class PassageCapacityRepository(BaseRepository):
    @property
    def collection(self) -> Collection:
        return passage_capacity_status_collection

    @parse_as(response_type=list[PassageCapacityStatus])
    def get_all_passage_capacity_status(self):
        return self.collection.find({})
