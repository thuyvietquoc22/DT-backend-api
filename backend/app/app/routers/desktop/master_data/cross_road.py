from fastapi import APIRouter

from app.domain.desktop.master_data.cross_road import cross_road_domain, CrossRoadDomain
from app.models.desktop.master_data.cross_road import CrossRoadCreate, CrossRoadResponse
from app.routers import BaseRouter


class CrossRoadRouter(BaseRouter):

    @property
    def cross_road_domain(self) -> CrossRoadDomain:
        return cross_road_domain

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix='/cross-road', tags=['Desktop Master Data> Cross Road'])

        @router.get('', response_model=list[CrossRoadResponse])
        async def get_all_cross_road():
            return self.cross_road_domain.get_all_cross_road()

        @router.get('/district/{district_id}')
        async def get_cross_road_by_district_id(district_id: int):
            return self.cross_road_domain.get_cross_road_by_district_id(district_id)

        @router.get('/{cross_road_id}')
        async def get_cross_road_by_id(cross_road_id: str):
            return self.cross_road_domain.get_cross_road_by_id(cross_road_id)

        @router.post('')
        async def create_cross_road(creator_cross_road: CrossRoadCreate):
            self.cross_road_domain.create_cross_road(creator_cross_road)
            return {"message": "create cross road success"}

        return router
