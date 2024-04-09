from fastapi import APIRouter

from app.domain.desktop.master_data.connection_source import ConnectSourceDomain, connection_source_domain
from app.models.desktop.master_data.connect_source import ConnectSourceCreate, ConnectSourceUpdate
from app.routers import BaseRouter


class ConnectSourceRouter(BaseRouter):

    @property
    def connection_source_domain(self) -> ConnectSourceDomain:
        return connection_source_domain

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/connection-source", tags=["Desktop Master Data > Connection Source"])

        @router.get("")
        def get_connection_source():
            return self.connection_source_domain.get_connection_source()

        @router.get("/{connection_source_keyname}")
        def get_connection_source_by_keyname(connection_source_keyname: str):
            return self.connection_source_domain.get_connection_source_by_keyname(connection_source_keyname)

        @router.post("")
        def create_connection_source(connection_source_create: ConnectSourceCreate):
            self.connection_source_domain.create_connection_source(connection_source_create)
            return {"message": "Created connection source"}

        @router.put("/{connection_source_keyname}")
        def update_connection_source(connection_source_keyname: str, connection_source_update: ConnectSourceUpdate):
            self.connection_source_domain.update_connection_source(connection_source_keyname, connection_source_update)
            return {"message": "Updated connection source"}

        @router.delete("/{connection_source_keyname}")
        def delete_connection_source(connection_source_keyname: str):
            self.connection_source_domain.delete_connection_source(connection_source_keyname)
            return {"message": "Deleted connection source"}

        return router
