from pymongo.cursor import Cursor

from app.db.mongo_db import permission_collection


class RoleService:
    @staticmethod
    def get_all_permission():
        result: Cursor = permission_collection.find()
        return result


role_service: RoleService = RoleService()
