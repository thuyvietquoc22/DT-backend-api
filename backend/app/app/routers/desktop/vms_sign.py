from fastapi import APIRouter

from app.domain.desktop.vms_sign import vms_sign_domain, VMSSignDomain
from app.models.desktop.control.vms_sign import VMSSignController, VMSSignRequest
from app.models.desktop.vms_sign import VMSSignCreate, VMSSignUpdate
from app.models.pagination_model import Pageable
from app.routers import BaseRouter


class VMSSignRouter(BaseRouter):

    @property
    def vms_domain(self) -> VMSSignDomain:
        return vms_sign_domain

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/vms-sign", tags=["Desktop > VMS Sign"])

        @router.get("")
        def get_all_vms_sign():
            return self.vms_domain.get_all_vms_sign()

        @router.get("/{vms_sign_id}")
        def get_vms_sign_by_id(vms_sign_id: str):
            return self.vms_domain.get_vms_sign_by_id(vms_sign_id)

        @router.get("/model/{model_id}")
        def get_vms_sign_by_model_id(model_id: str):
            return self.vms_domain.get_vms_sign_by_model_id(model_id)

        @router.get("/nearby/{cross_road_id}")
        def get_vms_sign_nearby(cross_road_id: str):
            return self.vms_domain.get_vms_sign_nearby(cross_road_id)

        @router.post("")
        def create_vms_sign(vms_sign_create: VMSSignCreate):
            self.vms_domain.create_vms_sign(vms_sign_create)
            return {"message": "Created vms sign"}

        @router.put("/{vms_sign_id}")
        def update_vms_sign(vms_sign_id: str, vms_sign_update: VMSSignUpdate):
            self.vms_domain.update_vms_sign(vms_sign_id, vms_sign_update)
            return {"message": "Updated vms sign"}

        @router.delete("/{vms_sign_id}")
        def delete_vms_sign(vms_sign_id: str):
            self.vms_domain.delete_vms_sign(vms_sign_id)
            return {"message": "Deleted vms sign"}

        @router.post("/control/{vms_sign_id}")
        def delete_vms_sign(vms_sign_id: str, controller: VMSSignRequest):
            self.vms_domain.control_vms_sign(vms_sign_id, controller)
            return {"message": "Controlled vms sign"}

        @router.get("/control/history/{vms_sign_id}")
        def get_last_vms_sign_control(vms_sign_id: str, page: int = 1, limit=10):
            pageable = Pageable.of(page, limit)
            return self.vms_domain.get_history_vms_sign_control(vms_sign_id, pageable)

        return router