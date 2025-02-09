from fastapi import APIRouter

from app.models.desktop.traffic_light import TrafficLightCreate, TrafficLightUpdate
from app.routers import BaseRouter, DesktopTag
from app.sevices.desktop.traffic_light import TrafficLightService


class TrafficLightRouter(BaseRouter):

    @property
    def traffic_light_service(self) -> TrafficLightService:
        return TrafficLightService()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix='/traffic-lights', tags=DesktopTag().get("Traffic Light"))

        @router.get('')
        def get_all_traffic_light():
            return self.traffic_light_service.get_all_traffic_light()

        @router.get('/{traffic_light_id}')
        def get_traffic_light_by_id(traffic_light_id: str):
            return self.traffic_light_service.get_traffic_light_by_id(traffic_light_id)

        @router.get('/model/{model_id}')
        def get_traffic_light_by_model_id(model_id: str):
            return self.traffic_light_service.get_traffic_light_by_model_id(model_id)

        @router.get('/nearby/{cross_road_id}')
        def get_traffic_light_nearby(cross_road_id: str):
            return self.traffic_light_service.get_traffic_light_nearby(cross_road_id)

        @router.get('/cross-road/{cross_road_id}')
        def get_traffic_light_by_cross_road_id(cross_road_id: str):
            return self.traffic_light_service.get_traffic_light_by_cross_road_id(cross_road_id)

        @router.post('')
        def create_traffic_light(traffic_light: TrafficLightCreate):
            self.traffic_light_service.create_traffic_light(traffic_light)
            return {
                "message": "Created traffic light"
            }

        @router.put('/{traffic_light_id}')
        def update_traffic_light(traffic_light_id: str, traffic_light: TrafficLightUpdate):
            self.traffic_light_service.update_traffic_light(traffic_light_id, traffic_light)
            return {
                "message": "Updated traffic light"
            }

        @router.delete('/{traffic_light_id}')
        def delete_traffic_light(traffic_light_id: str):
            self.traffic_light_service.delete_traffic_light(traffic_light_id)
            return {
                "message": "Deleted traffic light"
            }

        return router
