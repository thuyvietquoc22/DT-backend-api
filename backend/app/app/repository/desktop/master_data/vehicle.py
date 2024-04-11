from pymongo.collection import Collection

from app.db.mongo_db import vehicle_type_collection
from app.decorator.parser import parse_as
from app.models.desktop.master_data.vehicle_type import VehicleTypeResponse
from app.repository.base_repository import BaseRepository


class VehicleTypeRepository(BaseRepository):
    @property
    def collection(self) -> Collection:
        return vehicle_type_collection

    @parse_as(list[VehicleTypeResponse])
    def get_all_vehicle_type(self):
        return self.collection.find({})
