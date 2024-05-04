from fastapi import APIRouter

from app.decorator import signleton
from app.models import IntBody
from app.models.desktop.master_data.vehicle_type import VehicleTypeUpdate
from app.routers import BaseRouter, CMSTag
from app.sevices.desktop.master_data.vehicle_type import VehicleTypeService


@signleton.singleton
class VehicleType(BaseRouter):

    def __init__(self):
        self.cms_tag = CMSTag().get("Vehicle Type", True)

        # Service
        self.vehicle_type_service = VehicleTypeService()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/vehicle-type", tags=self.cms_tag)

        @router.get("")
        def get_all_vehicle_type():
            return self.vehicle_type_service.get_all_vehicle_type()

        @router.patch("/{vehicle_type_id}")
        def update_vehicle_size(vehicle_type_id: str, body: IntBody):
            self.vehicle_type_service.update_size_vehicle_type(body.value, vehicle_type_id)
            return {"message": "Updated vehicle type"}

        @router.put("/{vehicle_type_id}")
        def update_vehicle_type(vehicle_type_id: str, vehicle_type: VehicleTypeUpdate):
            self.vehicle_type_service.update_vehicle_type(vehicle_type, vehicle_type_id)
            return {"message": "Updated vehicle type"}


        return router
