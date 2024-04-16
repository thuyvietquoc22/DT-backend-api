from typing import List

from bson import ObjectId
from fastapi import APIRouter

from app.db.mongo_db import permission_collection
from app.routers import BaseRouter, CMSTag
from app.sevices.cms.permission import PermissionService
from app.models.cms.permission import PermissionResponse


class PermissionRouter(BaseRouter):

    def __init__(self):
        self.permission_service = PermissionService()

    @property
    def router(self):
        api_router = APIRouter(prefix='/permissions', tags=CMSTag().get("Permission"))

        @api_router.get('', response_model=List[PermissionResponse])
        async def get_permissions():
            result = self.permission_service.get_all()
            return result

        @api_router.post('', response_model=List[PermissionResponse])
        async def create_permission(permissions: List[PermissionResponse]):

            for i in permissions:
                if i.sub_permissions is not None:
                    for j in i.sub_permissions:
                        j.id = ObjectId()

            result = permission_collection.insert_many(
                [permission.model_dump(by_alias=True, exclude=["id"]) for
                 permission in permissions])

            return result.inserted_ids

        @api_router.post('/check')
        async def check_permission_id(permission_ids: list[str]):
            result = self.permission_service.get_all_by_id(permission_ids)
            return result

        return api_router
