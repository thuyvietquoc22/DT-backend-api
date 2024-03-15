from typing import List

from fastapi import APIRouter

from app.db.mongo_db import permission_collection
from app.domain.admin.permission import PermissionDomain
from app.models.admin.permission import PermissionModel


class PermissionRouter:

    def __init__(self, domain: PermissionDomain):
        self.domain = domain

    @property
    def router(self):
        api_router = APIRouter(prefix='/permissions', tags=['Permission in system'])

        @api_router.get('', response_model=List[PermissionModel])
        async def get_permissions():
            result = self.domain.get_all_permission()
            return result

        @api_router.post('', response_model=List[PermissionModel])
        async def create_permission(permission: List[PermissionModel]):
            return permission_collection.insert_many([permission.model_dump(by_alias=True, exclude=["id"]) for
                                                      permission in permission])

        return api_router
