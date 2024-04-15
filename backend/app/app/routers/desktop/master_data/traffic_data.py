from fastapi import APIRouter

from app.sevices.desktop.traffic_data import TrafficDataService
from app.models.desktop.traffic_data import TrafficDataCreate, TrafficDataResponse
from app.routers import BaseRouter


class TrafficDataRouter(BaseRouter):

    def __init__(self):
        self.traffic_service = TrafficDataService()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/traffic-data", tags=["Traffic Data"])

        @router.post("/add-data")
        def insert_traffic_data(data: list[TrafficDataCreate]):
            self.traffic_service.insert_traffic_data(data)
            return {"message": "Insert traffic data successfully"}

        @router.get("/get-data/{device_id}/{minute}", response_model=list[TrafficDataResponse])
        def get_traffic_data_by_camera_id(device_id: str, minute: int):
            result = self.traffic_service.get_traffic_data_by_camera_id(device_id, minute)
            return result

        return router
