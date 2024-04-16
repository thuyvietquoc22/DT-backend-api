from typing import List

from fastapi import APIRouter

from app.models.desktop.master_data.address import ProvinceListResponse, ProvinceResponse
from app.routers import BaseRouter, DesktopTag, CMSTag
from app.sevices.desktop.master_data.address import AddressService


class DesktopAddressRouter(BaseRouter):

    def __init__(self):
        name = "Address"
        self.tag = DesktopTag().get(name, False)
        self.desktop_master_tag = DesktopTag().get(name, True)
        self.cms_master_tag = CMSTag().get(name, True)

    @property
    def address_service(self) -> AddressService:
        return AddressService()

    @property
    def router(self):
        router = APIRouter(prefix='/address', tags=self.cms_master_tag)

        @router.get('/provinces', response_model=List[ProvinceListResponse], tags=self.desktop_master_tag)
        def get_all_provinces(name: str = ""):
            return self.address_service.get_all_provinces(name)

        @router.get('/provinces/{code}', response_model=ProvinceResponse, tags=self.desktop_master_tag)
        def get_province_by_id(code: int):
            return self.address_service.get_province_by_code(code)

        return router
