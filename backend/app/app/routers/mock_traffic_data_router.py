from datetime import datetime

from fastapi import APIRouter

from app.db.mongo_db import traffic_data_collection
from app.models.desktop.traffic_data import TrafficDataCreate
from app.routers import BaseRouter


class MockTrafficDataRouter(BaseRouter):
    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/mock-traffic-data", tags=["Mock Traffic Data"])

        @router.post("/add")
        def get_all_mock_traffic_data(data: list[TrafficDataCreate]):
            for item in data:
                item.time = datetime.now()
            return traffic_data_collection.insert_many([i.dict() for i in data])

        return router
