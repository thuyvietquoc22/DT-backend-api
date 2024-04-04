from fastapi import APIRouter

from app.routers import BaseRouter
from app.routers.desktop.address import DesktopAddressRouter
from app.routers.desktop.camara import CameraRouter
from app.routers.desktop.cross_road import CrossRoadRouter


class DesktopRouter:

    @property
    def router(self):
        api_router = APIRouter(prefix='/desktop')

        routers: list[BaseRouter] = [
            DesktopAddressRouter(),
            CrossRoadRouter(),
            CameraRouter()
        ]

        for router in routers:
            api_router.include_router(router.router)

        return api_router
