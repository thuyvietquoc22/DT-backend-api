from typing import List

from fastapi import APIRouter

from app.routers import BaseRouter, CMSTag
from app.sevices.cms.role import RoleService
from app.models.cms.role import RoleCreate, RoleResponse


class RoleRouter(BaseRouter):

    def __init__(self):
        self.role_service = RoleService

    @property
    def router(self):
        api_router = APIRouter(prefix='/roles', tags=CMSTag().get("Role"))

        @api_router.get('', response_model=List[RoleResponse])
        async def get_oles(role_name: str = None):
            result = self.role_service.get_all_role(role_name)
            return result

        @api_router.post("")
        async def create_role(permission_create: RoleCreate):
            result = self.role_service.create_role(permission_create)
            return {
                "message": f"Tạo thành công vai trò \"{permission_create.name}\".",
            }

        @api_router.post("/count-usage/{role_id}")
        async def count_role_usage(role_id: str):
            result = self.role_service.count_role_usage(role_id)
            return {
                "count": result,
            }

        @api_router.delete("/{role_id}")
        async def delete_role(role_id: str):
            result = self.role_service.delete_role(role_id)
            return {
                "message": f"Xóa thành công vai trò.",
            }

        return api_router
