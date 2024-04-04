from fastapi import APIRouter

from app.domain.desktop.traffic_light import TrafficLightDomain, traffic_light_domain
from app.models.desktop.traffic_light import TrafficLightCreate, TrafficLightUpdate
from app.routers import BaseRouter


class TrafficLightRouter(BaseRouter):

    @property
    def traffic_light_domain(self) -> TrafficLightDomain:
        return traffic_light_domain

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix='/traffic-lights', tags=['Desktop > Traffic Light'])

        @router.get('')
        def get_all_traffic_light():
            return self.traffic_light_domain.get_all_traffic_light()

        @router.get('/{traffic_light_id}')
        def get_traffic_light_by_id(traffic_light_id: str):
            return self.traffic_light_domain.get_traffic_light_by_id(traffic_light_id)

        @router.post('')
        def create_traffic_light(traffic_light: TrafficLightCreate):
            self.traffic_light_domain.create_traffic_light(traffic_light)
            return {
                "message": "Created traffic light"
            }

        @router.put('/{traffic_light_id}')
        def update_traffic_light(traffic_light_id: str, traffic_light: TrafficLightUpdate):
            self.traffic_light_domain.update_traffic_light(traffic_light_id, traffic_light)
            return {
                "message": "Updated traffic light"
            }


        @router.delete('/{traffic_light_id}')
        def delete_traffic_light(traffic_light_id: str):
            self.traffic_light_domain.delete_traffic_light(traffic_light_id)
            return {
                "message": "Deleted traffic light"
            }

        return router
