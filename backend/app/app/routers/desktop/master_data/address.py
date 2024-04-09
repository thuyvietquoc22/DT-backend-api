from typing import List

from fastapi import APIRouter

from app.domain.desktop.master_data.address import address_domain, AddressDomain
from app.models.desktop.master_data.address import ProvinceListResponse, ProvinceResponse
from app.routers import BaseRouter


class DesktopAddressRouter(BaseRouter):

    @property
    def address_domain(self) -> AddressDomain:
        return address_domain

    @property
    def router(self):
        router = APIRouter(prefix='/address', tags=['Desktop MasterData > Address'])

        @router.get('/provinces', response_model=List[ProvinceListResponse])
        def get_all_provinces(name: str = ""):
            return self.address_domain.get_all_provinces(name)

        @router.get('/provinces/{code}', response_model=ProvinceResponse)
        def get_province_by_id(code: int):
            return self.address_domain.get_province_by_code(code)

        return router
