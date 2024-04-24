from typing import Literal

from fastapi import APIRouter, UploadFile, Form, Query

from app.sevices.desktop.master_data.vms_component import VMSComponentService
from app.models.desktop.master_data.vms_component import VMSComponentResponse, VMSComponentUpdate
from app.routers import BaseRouter, DesktopTag, CMSTag


class VMSComponentRouter(BaseRouter):

    def __init__(self):
        # Swagger tag
        name = "VMS Component"
        self.tag = DesktopTag().get(name, False)
        self.desktop_master_tag = DesktopTag().get(name, True)
        self.cms_master_tag = CMSTag().get(name, True)

        self.vms_component_service = VMSComponentService()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/vms-components", tags=self.cms_master_tag)

        @router.get("", response_model=list[VMSComponentResponse], tags=self.desktop_master_tag)
        def get_vms_component():
            return self.vms_component_service.get_all_vms_component()

        @router.get("/type", response_model=list[VMSComponentResponse], tags=self.desktop_master_tag)
        def get_vms_component_by_tag(type_component: Literal["IMAGE", "ARROW"] = Query(alias="type")):
            return self.vms_component_service.get_vms_component_by_type(type_component)

        @router.get("/{vms_component_id}", response_model=VMSComponentResponse, tags=self.desktop_master_tag)
        def get_vms_component_by_id(vms_component_id: str):
            return self.vms_component_service.get_vms_component_by_id(vms_component_id)

        @router.get("/code/{code}", response_model=VMSComponentResponse, tags=self.desktop_master_tag)
        def get_vms_component_by_code(code: int):
            return self.vms_component_service.get_vms_component_by_code(code)

        @router.post("")
        def create_vms_component(
                image: UploadFile,
                name: str = Form(),
                type_component: Literal["IMAGE", "ARROW"] = Form(),
                code: int = Form(),
                category_key: str = Form(),
                meaning: str = Form()
        ):
            self.vms_component_service.create_vms_component(
                image=image,
                name=name,
                type_component=type_component,
                code=code,
                category_key=category_key,
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
