from fastapi import APIRouter

from app.models.desktop.master_data.cross_road import CrossRoadCreate, CrossRoadResponse, CrossRoadUpdate
from app.models.pagination_model import Pageable, PaginationResponse
from app.routers import BaseRouter
from app.sevices.desktop.master_data.cross_road import CrossRoadService


class CrossRoadRouter(BaseRouter):

    @property
    def cross_road_service(self) -> CrossRoadService:
        return CrossRoadService()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix='/cross-road', tags=['Desktop Master Data> Cross Road'])

        @router.get('', response_model=PaginationResponse[CrossRoadResponse])
        async def get_all_cross_road(limit: int = 10, page: int = 1):
            pageable: Pageable = Pageable.of(page, limit)
            result = self.cross_road_service.get_all_cross_road(pageable)
            return PaginationResponse.response_pageable(result, pageable)

        @router.get('/district/{district_id}', response_model=PaginationResponse[CrossRoadResponse])
        async def get_cross_road_by_district_id(district_id: int, limit: int = 10, page: int = 1):
            pageable = Pageable.of(page, limit)
            result = self.cross_road_service.get_cross_road_by_district_id(district_id, pageable)
            return PaginationResponse.response_pageable(result, pageable)

        @router.get('/{cross_road_id}')
        async def get_cross_road_by_id(cross_road_id: str):
            return self.cross_road_service.get_cross_road_by_id(cross_road_id)

        @router.post('')
        async def create_cross_road(creator_cross_road: CrossRoadCreate):
            self.cross_road_service.create_cross_road(creator_cross_road)
            return {"message": "create cross road success"}

        @router.put('/{district_id}')
        async def update_cross_road(district_id: str, cross_road_update: CrossRoadUpdate):
            self.cross_road_service.update_cross_road(district_id, cross_road_update)
            return {"message": "update cross road success"}

        return router
