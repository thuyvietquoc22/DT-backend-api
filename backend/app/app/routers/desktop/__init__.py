from fastapi import APIRouter

from app.routers import BaseRouter
from app.routers.desktop.camera import CameraRouter
from app.routers.desktop.master_data.address import DesktopAddressRouter
from app.routers.desktop.master_data.connection_source import ConnectSourceRouter
from app.routers.desktop.master_data.cross_road import CrossRoadRouter
from app.routers.desktop.master_data.vms_component import VMSComponentRouter
from app.routers.desktop.traffic_light import TrafficLightRouter
from app.routers.desktop.vms_sign import VMSSignRouter


class DesktopRouter:

    @property
    def router(self):
        api_router = APIRouter(prefix='/desktop')

        routers: list[BaseRouter] = [
            DesktopAddressRouter(),
            CrossRoadRouter(),
            ConnectSourceRouter(),
            VMSComponentRouter(),
            CameraRouter(),
            TrafficLightRouter(),
            VMSSignRouter(),
        ]

        for router in routers:
            api_router.include_router(router.router)

        return api_router
