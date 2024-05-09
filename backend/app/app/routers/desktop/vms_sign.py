from fastapi import APIRouter

from app.models.desktop.control.vms_sign import VMSSignRequest
from app.models.desktop.vms_sign import VMSSignCreate, VMSSignUpdate
from app.models.pagination_model import Pageable
from app.routers import BaseRouter, DesktopTag
from app.sevices.desktop.master_data.vms_component import VMSComponentService
from app.sevices.desktop.vms_sign import VMSSignService


class VMSSignRouter(BaseRouter):

    @property
    def vms_service(self) -> VMSSignService:
        return VMSSignService()

    @property
    def vms_component_service(self) -> VMSComponentService:
        return VMSComponentService()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/vms-sign", tags=DesktopTag().get("VMS Sign"))

        @router.get("")
        def get_all_vms_sign():
            return self.vms_service.get_all_vms_sign()

        @router.get("/{vms_sign_id}")
        def get_vms_sign_by_id(vms_sign_id: str):
            return self.vms_service.get_vms_sign_by_id(vms_sign_id)

        @router.get("/model/{model_id}")
        def get_vms_sign_by_model_id(model_id: str):
            return self.vms_service.get_vms_sign_by_model_id(model_id)

        @router.get("/nearby/{cross_road_id}")
        def get_vms_sign_nearby(cross_road_id: str):
            return self.vms_service.get_vms_sign_nearby(cross_road_id)

        @router.post("")
        def create_vms_sign(vms_sign_create: VMSSignCreate):
            self.vms_service.create_vms_sign(vms_sign_create)
            return {"message": "Created vms sign"}

        @router.put("/{vms_sign_id}")
        def update_vms_sign(vms_sign_id: str, vms_sign_update: VMSSignUpdate):
            self.vms_service.update_vms_sign(vms_sign_id, vms_sign_update)
            return {"message": "Updated vms sign"}

        @router.delete("/{vms_sign_id}")
        def delete_vms_sign(vms_sign_id: str):
            self.vms_service.delete_vms_sign(vms_sign_id)
            return {"message": "Deleted vms sign"}

        @router.post("/control/{vms_sign_id}")
        def delete_vms_sign(vms_sign_id: str, controller: VMSSignRequest):
            self.vms_service.control_vms_sign(vms_sign_id, controller)
            return {"message": "Controlled vms sign"}

        @router.get("/control/history/{vms_sign_id}")
        def get_last_vms_sign_control(vms_sign_id: str, page: int = 1, limit=10):
            pageable = Pageable.of(page, limit)
            return self.vms_service.get_history_vms_sign_control(vms_sign_id, pageable)

        @router.get("/control/current/{vms_sign_id}")
        def get_current_state_vms_sign_control(vms_sign_id: str):
            result = self.vms_service.get_current_state_vms_sign_control(vms_sign_id)
            response = result.dict()
            for index, model_id in enumerate(result.images):
                model = self.vms_component_service.get_vms_component_by_id(model_id.vms_component_id)
                response.get("images")[index].update(model.dict())

            return response

        return router
