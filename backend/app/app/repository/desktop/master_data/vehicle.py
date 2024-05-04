from bson import ObjectId
from pymongo.collection import Collection

from app.db.mongo.vehicle_type import vehicle_type_collection
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

    def update_vehicle_type(self, value, vehicle_type_id: str):
        return self.collection.update_one({"_id": ObjectId(vehicle_type_id)}, {"$set": {"size": value}})

    @parse_as(VehicleTypeResponse, True)
    def get_vehicle_type(self, vehicle_type_id):
        pipeline = self.root_pipeline

        return self.collection.aggregate(pipeline)
