from typing import List

from fastapi import APIRouter

from app.domain.admin.role import RoleDomain
from app.models.admin.permission import PermissionResponse
from app.models.admin.role import RoleCreate, RoleResponse


class RoleRouter:

    def __init__(self, domain: RoleDomain):
        self.domain = domain

    @property
    def router(self):
        api_router = APIRouter(prefix='/roles', tags=['Permission & Role'])

        @api_router.get('', response_model=List[RoleResponse])
        async def get_oles(role_name: str = None):
            result = self.domain.get_all_role(role_name)
            return result

        @api_router.post("")
        async def create_role(permission_create: RoleCreate):
            result = self.domain.create_role(permission_create)
            return {
                "message": f"Tạo thành công vai trò \"{permission_create.name}\".",
            }

        @api_router.post("/count-usage/{role_id}")
        async def count_role_usage(role_id: str):
            result = self.domain.count_role_usage(role_id)
            return {
                "count": result,
            }

        @api_router.delete("/{role_id}")
        async def delete_role(role_id: str):
            result = self.domain.delete_role(role_id)
            return {
                "message": f"Xóa thành công vai trò.",
            }

        return api_router
