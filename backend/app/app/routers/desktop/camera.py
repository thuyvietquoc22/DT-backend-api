from botocore.paginate import PaginatorModel
from fastapi import APIRouter

from app.sevices.desktop.camera import CameraService
from app.models.desktop.camera import CameraCreate, CameraUpdate
from app.models.desktop.control.camera import CameraControl, CameraControlRequest
from app.models.pagination_model import Pageable, PaginationResponse
from app.routers import BaseRouter


class CameraRouter(BaseRouter):

    @property
    def camera_service(self) -> CameraService:
        return CameraService()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix='/camera', tags=['Desktop > Camera'])

        @router.get('')
        async def get_all_camera():
            return self.camera_service.get_all_camera()

        @router.get('/{camera_id}')
        async def get_camera_by_id(camera_id: str):
            return self.camera_service.get_camera_by_id(camera_id)

        @router.get('/model/{model_id}')
        async def get_camera_by_model_id(model_id: str):
            return self.camera_service.get_camera_by_model_id(model_id)

        @router.get('/nearby/{cross_road_id}')
        async def get_camera_nearby(cross_road_id: str):
            return self.camera_service.get_camera_nearby(cross_road_id)

        @router.post('')
        async def create_camera(camera: CameraCreate):
            return self.camera_service.create_camera(camera)

        @router.put('/{camera_id}')
        async def update_camera(camera_id: str, camera: CameraUpdate):
            self.camera_service.update_camera(camera_id, camera)
            return {
                "message": "Update camera successfully."
            }

        @router.delete('/{camera_id}')
        async def delete_camera(camera_id: str):
            self.camera_service.delete_camera(camera_id)
            return {
                "messsage": "Camera deleted."
            }

        @router.post('/control')
        async def control_camera(camera_control: CameraControlRequest):
            self.camera_service.control_camera(camera_control)
            return {
                "message": "Controlled successfully."
            }

        @router.get('/control/history/{device_id}', response_model=PaginationResponse[CameraControl])
        async def get_last_camera_control(device_id: str, page: int = 1, limit=10):
            pageable = Pageable.of(page, limit)
            result = self.camera_service.get_history_control(device_id, pageable)
            return PaginationResponse.response_pageable(result, pageable)

        return router
