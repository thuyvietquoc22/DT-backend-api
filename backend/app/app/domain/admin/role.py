from bson import ObjectId

from app.decorator.parser import parse_as
from app.domain.admin.permission import permission_domain
from app.models.admin.role import RoleCreate, RoleResponse
from app.repository.admin.role import RoleRepository


class RoleDomain:

    def __init__(self, role_repo: RoleRepository):
        self.role_repo = role_repo

    def get_all_role(self, role_name: str = None):
        result = self.role_repo.get_all_role(role_name)
        return result

    def create_role(self, permission_create: RoleCreate):
        permission_create.permission_ids = [ObjectId(permission_id) for permission_id in
                                            permission_create.permission_ids]
        return self.role_repo.create(permission_create)

    def get_permission_by_role_id(self, role_id: str):
        return self.role_repo.get_permission_by_role_by_id(role_id)

    def delete_role(self, role_id):
        return self.role_repo.delete(role_id)

    def count_role_usage(self, _id: str):
        return self.role_repo.count_role_usage(_id)


role_domain = RoleDomain(RoleRepository())
