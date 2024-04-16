from fastapi import APIRouter

from app.models.desktop.traffic_data import TrafficDataCreate, TrafficDataResponse
from app.routers import BaseRouter, DesktopTag, CMSTag
from app.sevices.desktop.traffic_data import TrafficDataService


class TrafficDataRouter(BaseRouter):

    def __init__(self):
        # Swagger Tags
        name = "Traffic Data"
        self.tag = DesktopTag().get(name, False)
        self.desktop_master_tag = DesktopTag().get(name, True)
        self.cms_master_tag = CMSTag().get(name, True)

        self.traffic_service = TrafficDataService()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/traffic-data", tags=self.cms_master_tag)

        @router.post("/add-data")
        def insert_traffic_data(data: list[TrafficDataCreate]):
            self.traffic_service.insert_traffic_data(data)
            return {"message": "Insert traffic data successfully"}

        @router.get("/get-data/{device_id}/{minute}",
                    response_model=list[TrafficDataResponse],
                    tags=self.desktop_master_tag)
        def get_traffic_data_by_camera_id(device_id: str, minute: int):
            result = self.traffic_service.get_traffic_data_by_camera_id(device_id, minute)
            return result

        return router
