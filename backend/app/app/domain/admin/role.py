from bson import ObjectId

from app.decorator.parser import parse_as
from app.domain.admin.permission import permission_domain
from app.models.admin.role import RoleCreate, RoleResponse
from app.repository.admin.role import RoleRepository


class RoleDomain:

    def __init__(self, role_repo: RoleRepository):
        self.role_repo = role_repo

    def get_all_role(self):
        return self.role_repo.get_all_role()

    @parse_as(response_type=RoleResponse)
    def create_role(self, permission_create: RoleCreate):
        valid_permissions = permission_domain.get_all_by_id(permission_create.permission_ids)
        valid_ids = [ObjectId(i.id) for i in valid_permissions]
        permission_create.permission_ids = valid_ids
        return self.role_repo.create(permission_create)

    def get_permission_by_role_id(self, role_id: str):
        return self.role_repo.get_permission_by_role_by_id(role_id)


role_domain = RoleDomain(RoleRepository())
