from fastapi import APIRouter

from app.sevices.desktop.master_data.street import StreetService
from app.models.desktop.master_data.street import StreetResponse, StreetCreate, StreetUpdate
from app.repository.desktop.master_data.street import StreetRepository
from app.routers import BaseRouter, DesktopTag, CMSTag


class StreetRouter(BaseRouter):

    def __init__(self):
        name = "Street"
        self.tag = DesktopTag().get(name, False)
        self.desktop_master_tag = DesktopTag().get(name, True)
        self.cms_master_tag = CMSTag().get(name, True)

        self.street_service = StreetService()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/streets", tags=self.cms_master_tag)

        @router.get("/districts/{districts_code}", response_model=list[StreetResponse], tags=self.desktop_master_tag)
        def get_all_street(districts_code: int):
            return self.street_service.find_all_by_districts(districts_code)

        @router.post("")
        def create_street(street_create: StreetCreate):
            self.street_service.create_street(street_create)
            return {"message": "Created street"}

        @router.put("/{street_id}")
        def update_street(street_id: str, street_create: StreetUpdate):
            self.street_service.update_street(street_id, street_create)
            return {"message": "Updated street"}

        @router.delete("/{street_id}")
        def delete_street(street_id: str):
            self.street_service.delete_street(street_id)
            return {"message": "Deleted street"}

        return router
