from typing import List

from fastapi import APIRouter

from app.domain.admin.role import RoleDomain
from app.models.admin.permission import PermissionResponse
from app.models.admin.role import RoleCreate


class RoleRouter:

    def __init__(self, domain: RoleDomain):
        self.domain = domain

    @property
    def router(self):
        api_router = APIRouter(prefix='/roles', tags=['Permission & Role'])

        @api_router.get('', response_model=List[PermissionResponse])
        async def get_roles():
            result = self.domain.get_all_role()
            return result

        @api_router.post("")
        async def create_role(permission_create: RoleCreate):
            result = self.domain.create_role(permission_create)
            return result

        return api_router
