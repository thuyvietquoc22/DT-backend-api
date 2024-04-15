from typing import Literal

from fastapi import APIRouter, UploadFile, Form

from app.sevices.desktop.master_data.vms_component import VMSComponentService
from app.models.desktop.master_data.vms_component import VMSComponentResponse, VMSComponentUpdate
from app.routers import BaseRouter


class VMSComponentRouter(BaseRouter):

    def __init__(self):
        self.vms_component_service = VMSComponentService()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/vms-components", tags=["Desktop Master Data > VMS Component"])

        @router.get("", response_model=list[VMSComponentResponse])
        def get_vms_component():
            return self.vms_component_service.get_all_vms_component()

        @router.get("/{vms_component_id}", response_model=VMSComponentResponse)
        def get_vms_component_by_id(vms_component_id: str):
            return self.vms_component_service.get_vms_component_by_id(vms_component_id)

        @router.get("/code/{code}", response_model=VMSComponentResponse)
        def get_vms_component_by_code(code: int):
            return self.vms_component_service.get_vms_component_by_code(code)

        @router.post("")
        def create_vms_component(
                image: UploadFile,
                name: str = Form(),
                type_component: Literal["IMAGE", "ARROW"] = Form(),
                code: int = Form(),
                meaning: str = Form()
        ):
            self.vms_component_service.create_vms_component(
                image=image,
                name=name,
                type_component=type_component,
                code=code,
                meaning=meaning
            )
            return {"message": "VMS Component created."}

        @router.put("/{vms_component_id}")
        def update_vms_component(vms_component_id: str, update_data: VMSComponentUpdate):
            self.vms_component_service.update_vms_component(vms_component_id, update_data)
            return {"message": "VMS Component updated."}

        @router.patch("/image/{vms_component_id}")
        def update_vms_component_image(vms_component_id: str, image: UploadFile):
            self.vms_component_service.update_vms_component_image(vms_component_id, image)
            return {"message": "VMS component updated new image."}

        @router.delete("/{vms_component_id}")
        def delete_vms_component(vms_component_id: str):
            self.vms_component_service.delete_vms_component(vms_component_id)
            return {"message": "VMS Component deleted."}

        return router
