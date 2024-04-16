from fastapi import APIRouter

from app.models.desktop.master_data.connect_source import ConnectSourceCreate, ConnectSourceUpdate
from app.routers import BaseRouter, DesktopTag, CMSTag
from app.sevices.desktop.master_data.connection_source import ConnectSourceService


class ConnectSourceRouter(BaseRouter):
    def __init__(self):
        name = "Connection Source"
        self.tag = DesktopTag().get(name, False)
        self.desktop_master_tag = DesktopTag().get(name, True)
        self.cms_master_tag = CMSTag().get(name, True)

    @property
    def connection_source_service(self) -> ConnectSourceService:
        return ConnectSourceService()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/connection-source", tags=self.cms_master_tag)

        @router.get("", tags=self.desktop_master_tag)
        def get_connection_source():
            return self.connection_source_service.get_connection_source()

        @router.get("/{connection_source_keyname}", tags=self.desktop_master_tag)
        def get_connection_source_by_keyname(connection_source_keyname: str):
            return self.connection_source_service.get_connection_source_by_keyname(connection_source_keyname)

        @router.post("")
        def create_connection_source(connection_source_create: ConnectSourceCreate):
            self.connection_source_service.create_connection_source(connection_source_create)
            return {"message": "Created connection source"}

        @router.put("/{connection_source_keyname}")
        def update_connection_source(connection_source_keyname: str, connection_source_update: ConnectSourceUpdate):
            self.connection_source_service.update_connection_source(connection_source_keyname, connection_source_update)
            return {"message": "Updated connection source"}

        @router.delete("/{connection_source_keyname}")
        def delete_connection_source(connection_source_keyname: str):
            self.connection_source_service.delete_connection_source(connection_source_keyname)
            return {"message": "Deleted connection source"}

        return router
