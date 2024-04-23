from pymongo.collection import Collection

from app.db.mongo_db import bus_connection_collection
from app.models.desktop.master_data.bus_connection import BusConnectionCreate
from app.repository.base_repository import BaseRepository


class BusConnectionRepository(BaseRepository):
    @property
    def collection(self) -> Collection:
        return bus_connection_collection

    def create_bus_connection(self, bus_connections: list[BusConnectionCreate]):
        obj = [bs.model_dump(by_alias=True, exclude={"id"}) for bs in bus_connections]
        return self.collection.insert_many(obj)

    def list_bus_connections(self, pageable):
        return self.get_all(pageable)





