from pymongo.collection import Collection

from app.db.mongo_db import connection_source
from app.decorator.parser import parse_as
from app.models.desktop.master_data.connect_source import ConnectSourceResponse
from app.repository.base_repository import BaseRepository


class ConnectSourceRepository(BaseRepository):
    @property
    def collection(self) -> Collection:
        return connection_source

    @parse_as(list[ConnectSourceResponse])
    def find_all_connection_source(self):
        return self.collection.find({})

    @parse_as(ConnectSourceResponse)
    def find_connection_source_by_keyname(self, keyname: str):
        return self.collection.find_one({"keyname": keyname})

    def update_connection_source(self, connection_source_keyname, connection_source_update):
        return self.collection.update_one({"keyname": connection_source_keyname},
                                          {"$set": connection_source_update.dict(exclude_none=True)})

    def delete_by_keyname(self, connection_source_keyname):
        return self.collection.delete_one({"keyname": connection_source_keyname})

