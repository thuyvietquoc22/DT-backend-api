from typing import Literal

from fastapi import APIRouter, Query

from app.models.desktop.master_data.vms_component_category import VMSComponentCategoryResponse
from app.routers import BaseRouter, CMSTag, DesktopTag
from app.sevices.desktop.master_data.vms_component_category import VMSComponentCategoryService


class VMSComponentCategoryRouter(BaseRouter):
    def __init__(self):
        self.vms_component_cate_service = VMSComponentCategoryService()
        self.cms_tag = CMSTag().get("VMS Component Category", True)
        self.desktop_tag = DesktopTag().get("VMS Component Category")

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/vms-component-categories", tags=self.cms_tag)

        @router.get("", tags=self.desktop_tag, response_model=list[VMSComponentCategoryResponse])
        def get_all_vms_component_categories():
            return self.vms_component_cate_service.get_all_vms_component_categories()

        @router.get("/type", tags=self.desktop_tag, response_model=list[VMSComponentCategoryResponse])
        def get_all_vms_component_categories_by_type(component_type: Literal["IMAGE", "ARROW"] = Query(alias="type")):
            return self.vms_component_cate_service.get_all_vms_component_categories_by_type(component_type)

        return router
