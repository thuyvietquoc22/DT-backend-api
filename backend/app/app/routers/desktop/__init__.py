from fastapi import APIRouter

from app.routers import BaseRouter, BaseRouterGroup
from app.routers.desktop.camera import CameraRouter
from app.routers.desktop.master_data.address import DesktopAddressRouter
from app.routers.desktop.master_data.bus_connection import BusConnectionRouter
from app.routers.desktop.master_data.bus_routes import BusRoutesRouter
from app.routers.desktop.master_data.connection_source import ConnectSourceRouter
from app.routers.desktop.master_data.cross_road import CrossRoadRouter
from app.routers.desktop.master_data.street import StreetRouter
from app.routers.desktop.master_data.traffic_data import TrafficDataRouter
from app.routers.desktop.master_data.vehicle_type import VehicleType
from app.routers.desktop.master_data.vms_component import VMSComponentRouter
from app.routers.desktop.master_data.vms_component_category import VMSComponentCategoryRouter
from app.routers.desktop.passage_capacity import PassageCapacityRouter
from app.routers.desktop.traffic_light import TrafficLightRouter
from app.routers.desktop.vms_sign import VMSSignRouter


class DesktopRouter(BaseRouterGroup):

    @property
    def prefix(self) -> str:
        return "/desktop"

    @property
    def sub_routers(self) -> list[BaseRouter]:
        return [
            TrafficDataRouter(),
            BusRoutesRouter(),
            BusConnectionRouter(),

            DesktopAddressRouter(),
            CrossRoadRouter(),
            ConnectSourceRouter(),
            StreetRouter(),
            VMSComponentRouter(),
            VMSComponentCategoryRouter(),

            VehicleType(),
            PassageCapacityRouter(),

            CameraRouter(),
            TrafficLightRouter(),
            VMSSignRouter(),
        ]
