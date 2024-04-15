from bson import ObjectId

from app.decorator import signleton
from app.models.cms.role import RoleCreate
from app.repository.cms.role import RoleRepository


@signleton.singleton
class RoleService:

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


role_service = RoleService(RoleRepository())
