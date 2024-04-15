from fastapi import APIRouter

from app.domain.desktop.passage_capacity import PassageCapacityDomain
from app.models.desktop.passage_capacity import Bounce
from app.routers import BaseRouter
from app.utils.map_4d_service import Map4DService


class PassageCapacityRouter(BaseRouter):

    def __init__(self):
        self.passage_capacity_domain = PassageCapacityDomain()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/passage-capacity", tags=["Desktop > Passage Capacity"])

        @router.get("/bounce")
        def get_all_passage_capacity(min_lat: float, max_lat: float, min_lng: float, max_lng: float):
            bounce = Bounce(min_lat=min_lat, max_lat=max_lat, min_lng=min_lng, max_lng=max_lng)
            result, new_bounce = self.passage_capacity_domain.get_all_passage_capacity(bounce)
            return {
                "values": result,
                "center": new_bounce.center
            }

        @router.get("/keyword")
        def search_passage_capacity(keyword: str):
            result, new_bounce = self.passage_capacity_domain.get_passage_capacity_by_keyword(keyword)
            return {
                "values": result,
                "center": new_bounce.center
            }

        return router
