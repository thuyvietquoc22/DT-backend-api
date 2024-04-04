from fastapi import APIRouter

from app.domain.desktop.camera import CameraDomain, camera_domain
from app.models.desktop.camera import CameraCreate, CameraControl, CameraUpdate
from app.routers import BaseRouter


class CameraRouter(BaseRouter):

    @property
    def camera_domain(self) -> CameraDomain:
        return camera_domain

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix='/camera', tags=['Desktop > Camera'])

        @router.get('')
        async def get_all_camera():
            return self.camera_domain.get_all_camera()

        @router.post('')
        async def create_camera(camera: CameraCreate):
            return self.camera_domain.create_camera(camera)

        @router.get('/{camera_id}')
        async def get_camera_by_id(camera_id: str):
            return self.camera_domain.get_camera_by_id(camera_id)

        @router.get('/nearby/{cross_road_id}')
        async def get_camera_nearby(cross_road_id: str):
            return self.camera_domain.get_camera_nearby(cross_road_id)

        @router.put('/{camera_id}')
        async def update_camera(camera_id: str, camera: CameraUpdate):
            self.camera_domain.update_camera(camera_id, camera)
            return {
                "message": "Update camera successfully."
            }

        @router.post('/control')
        async def control_camera(camera_control: CameraControl):
            # Todo control camera
            return {
                "message": "This endpoint not implemented yet."
            }

        return router
