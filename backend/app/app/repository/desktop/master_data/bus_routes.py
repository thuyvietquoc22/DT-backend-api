from pymongo.collection import Collection

from app.db.mongo.bus_routes import bus_routes_collection
from app.decorator.parser import parse_as
from app.models.desktop.master_data.bus_routes import BusRoutesCreate, BusRoutesResponse, BusRoutesUpdate
from app.repository.base_repository import BaseRepository


class BusRoutesRepository(BaseRepository[BusRoutesResponse, BusRoutesCreate, BusRoutesUpdate]):
    @property
    def collection(self) -> Collection:
        return bus_routes_collection

    @property
    def root_pipeline(self):
        return [
            {'$lookup': {'from': 'model', 'localField': 'bus_stops_id', 'foreignField': '_id', 'as': 'bus_stops'}}
        ]

    @parse_as(BusRoutesResponse, True)
    def create_bus_router(self, bus_router: BusRoutesCreate):
        obj = bus_router.model_dump(by_alias=True, exclude={"id", "bus_connections"})
        inserted = self.collection.insert_one(obj)
        pipeline = [{"$match": {"_id": inserted.inserted_id}}] + self.root_pipeline
        return self.collection.aggregate(pipeline)
