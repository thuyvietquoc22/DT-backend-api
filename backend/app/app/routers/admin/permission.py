from typing import List

from fastapi import APIRouter

from app.db.mongo_db import permission_collection
from app.models.permission_model import PermissionModel
from app.services.role_service import role_service


class RoleRouter:

    @property
    def router(self):
        api_router = APIRouter(prefix='/roles', tags=['Role & Permission in system'])

        @api_router.get('', response_model=List[PermissionModel])
        async def get_permissions():
            result = role_service.get_all_permission()
            return result

        @api_router.post('', response_model=List[PermissionModel])
        async def create_permission(permission: List[PermissionModel]):
            return permission_collection.insert_many([permission.model_dump(by_alias=True, exclude=["id"]) for
                                                      permission in permission])

        return api_router


role_router = RoleRouter()
