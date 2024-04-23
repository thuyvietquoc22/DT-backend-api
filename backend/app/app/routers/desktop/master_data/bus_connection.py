from fastapi import APIRouter

from app.models.desktop.master_data.bus_connection import BusConnectionCreate
from app.models.desktop.master_data.bus_routes import BusStopResponse, BusRoutesCreate
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

        @router.post("")
        def create_bus_router(bus_router: BusConnectionCreate):
            result = self.bus_connect_service.create_bus_connection(bus_router)
            return result
            # return {"message": "Create bus router success"}

        return router
