from fastapi import APIRouter, Query

from app.models.desktop.master_data.cross_road import CrossRoadCreate, CrossRoadResponse, CrossRoadUpdate
from app.models.pagination_model import Pageable, PaginationResponse
from app.routers import BaseRouter, DesktopTag, CMSTag
from app.sevices.desktop.master_data.cross_road import CrossRoadService


class CrossRoadRouter(BaseRouter):

    def __init__(self):
        # Swagger Tag
        name = "Cross Road"
        self.tag = DesktopTag().get(name, False)
        self.desktop_master_tag = DesktopTag().get(name, True)
        self.cms_master_tag = CMSTag().get(name, True)

    @property
    def cross_road_service(self) -> CrossRoadService:
        return CrossRoadService()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix='/cross-road', tags=self.cms_master_tag)

        @router.get('', response_model=PaginationResponse[CrossRoadResponse], tags=self.desktop_master_tag)
        async def get_all_cross_road(limit: int = 10, page: int = 1):
            pageable: Pageable = Pageable.of(page, limit)
            result = self.cross_road_service.get_all_cross_road(pageable)
            return PaginationResponse.response_pageable(result, pageable)

        @router.get('/cross_location', tags=self.desktop_master_tag,
                    description="Lấy toạ độ điểm giao của 2 tuyến đường dựa trên <Tên> đường và quận/huyện")
        async def get_cross_road_location(
                first_street: str = Query(..., title="First street name"),
                second_street: str = Query(..., title="Second street name"),
                district: str = Query(..., title="District name")):
            return self.cross_road_service.get_cross_road_location(first_street, second_street, district)

        @router.get('/{cross_road_id}', tags=self.desktop_master_tag, )
        async def get_cross_road_by_id(cross_road_id: str):
            return self.cross_road_service.get_cross_road_by_id(cross_road_id)

        @router.get('/street/{street_id}', response_model=list[str],
                    description="Lấy danh sách id các tuyến đường đã được tạo nút giao với tuyến đường được gửi lên")
        async def get_cross_road_by_street_id(street_id: str):
            return self.cross_road_service.get_street_ids_existed_by_street_id(street_id)

        @router.get('/district/{district_id}', response_model=PaginationResponse[CrossRoadResponse],
                    tags=self.desktop_master_tag)
        async def get_cross_road_by_district_id(district_id: int, limit: int = 10, page: int = 1):
            pageable = Pageable.of(page, limit)
            result = self.cross_road_service.get_cross_road_by_district_id(district_id, pageable)
            return PaginationResponse.response_pageable(result, pageable)

        @router.post('')
        async def create_cross_road(creator_cross_road: CrossRoadCreate):
            self.cross_road_service.create_cross_road(creator_cross_road)
            return {"message": "create cross road success"}

        @router.put('/{district_id}')
        async def update_cross_road(district_id: str, cross_road_update: CrossRoadUpdate):
            self.cross_road_service.update_cross_road(district_id, cross_road_update)
            return {"message": "update cross road success"}

        @router.delete('/{cross_road_id}')
        async def delete_cross_road(cross_road_id: str):
            self.cross_road_service.delete_cross_road(cross_road_id)
            return {"message": "delete cross road success"}

        return router
