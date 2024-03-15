from pymongo.cursor import Cursor

from app.db.mongo_db import permission_collection
from app.repository.admin.permission import PermissionRepository


class PermissionDomain:

    def __init__(self, repo: PermissionRepository):
        self.repo = repo

    def get_all_permission(self):
        result: Cursor = self.repo.get_all()
        return result


permission_domain = PermissionDomain(PermissionRepository(permission_collection))
