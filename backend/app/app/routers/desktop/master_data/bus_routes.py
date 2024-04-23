from fastapi import APIRouter

from app.models.desktop.master_data.bus_routes import BusStopResponse, BusRoutesCreate, BusRoutesUpdate
from app.models.pagination_model import Pageable, PaginationResponse
from app.routers import BaseRouter, CMSTag
from app.sevices.desktop.master_data.bus_routes import BusRouteService


class BusRoutesRouter(BaseRouter):

    def __init__(self):
        self.cms_tag = CMSTag().get("Bus Routes", True)

        """
        Service injection
        """

        self.bus_route_service = BusRouteService()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/bus-routes", tags=self.cms_tag)

        @router.get("")
        def list_bus_routes(page: int = 1, limit: int = 10):
            pageable = Pageable(page=page, limit=limit)
            result = self.bus_route_service.list_bus_routes(pageable)
            return PaginationResponse.response_pageable(result, pageable)

        @router.post("")
        def create_bus_router(bus_router: BusRoutesCreate):
            result = self.bus_route_service.create_bus_router(bus_router)
            return result
            # return {"message": "Create bus router success"}

        @router.get("/{bus_routes_id}")
        def get_bus_router(bus_routes_id: str):
            result = self.bus_route_service.get_bus_router(bus_routes_id)
            return result

        @router.put("/{bus_routes_id}")
        def update_bus_router(bus_routes_id: str, bus_router: BusRoutesUpdate):
            result = self.bus_route_service.update_bus_router(bus_routes_id, bus_router)
            return {"message": "Update bus router success"}

        @router.delete("/{bus_routes_id}")
        def delete_bus_router(bus_routes_id: str):
            self.bus_route_service.delete_bus_router(bus_routes_id)
            return {"message": "Delete bus router success"}

        return router
