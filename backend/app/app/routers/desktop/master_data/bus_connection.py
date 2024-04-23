from fastapi import APIRouter

from app.models.desktop.master_data.bus_connection import BusConnectionCreate, BusConnectionUpdate
from app.models.desktop.master_data.bus_routes import BusStopResponse, BusRoutesCreate
from app.models.pagination_model import Pageable, PaginationResponse
from app.routers import BaseRouter, CMSTag
from app.sevices.desktop.master_data.bus_connection import BusConnectionService
from app.sevices.desktop.master_data.bus_routes import BusRouteService


class BusConnectionRouter(BaseRouter):

    def __init__(self):
        self.cms_tag = CMSTag().get("Bus Connection", True)

        """
        Service injection
        """

        self.bus_connect_service = BusConnectionService()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/bus-connection", tags=self.cms_tag)

        @router.get("")
        def list_bus_routes(page: int = 1, limit: int = 10):
            pageable = Pageable(page=page, limit=limit)
            result = self.bus_connect_service.list_bus_connections(pageable)
            return PaginationResponse.response_pageable(result, pageable)

        @router.post("")
        def create_bus_router(bus_router: BusConnectionCreate):
            result = self.bus_connect_service.create_bus_connection(bus_router)
            return result
            # return {"message": "Create bus router success"}

        @router.get("/{bus_connection_id}")
        def get_bus_router(bus_connection_id: str):
            result = self.bus_connect_service.get_bus_connection(bus_connection_id)
            return result

        @router.put("/{bus_connection_id}")
        def update_bus_router(bus_connection_id: str, bus_connection: BusConnectionUpdate):
            self.bus_connect_service.update_bus_connection(bus_connection_id, bus_connection)
            return {"message": "Update bus router success"}

        @router.delete("/{bus_connection_id}")
        def delete_bus_router(bus_connection_id: str):
            self.bus_connect_service.delete_bus_connection(bus_connection_id)
            return {"message": "Delete bus router success"}

        return router
