from bson import ObjectId
from pymongo.collection import Collection

from app.db.mongo.role import role_collection
from app.db.mongo.account import account_collection
from app.decorator.parser import parse_as
from app.models.cms.role import RoleResponse, RoleCreate, RoleUpdate
from app.repository.base_repository import BaseRepository


class RoleRepository(BaseRepository[RoleResponse, RoleCreate, RoleUpdate]):

    @property
    def collection(self) -> Collection:
        return role_collection

    @staticmethod
    def __filter_permission(role: RoleResponse):
        permission_ids = set(role.permission_ids)
        parent_permissions = []

        for permission in role.permissions:
            if permission.id in permission_ids:
                parent_permissions.append(permission)
            else:
                sub_permissions = [sub_permission for sub_permission in permission.sub_permissions if
                                   sub_permission.id in permission_ids]
                if sub_permissions:
                    # Lọc ra chỉ những sub_permission thỏa mãn điều kiện
                    permission.sub_permissions = sub_permissions
                    parent_permissions.append(permission)

        role.permissions = parent_permissions
        return role

    @parse_as(response_type=list[RoleResponse])
    def __get_all_role(self):
        pipeline = [
            {"$lookup": {
                "from": "permissions", "localField": "permission_ids", "foreignField": "_id", "as": "by_parent", }, },
            {"$lookup": {
                "from": "permissions",
                "localField": "permission_ids",
                "foreignField": "sub_permissions._id",
                "as": "by_child",
            },
            },
            {"$addFields": {
                "permissions": {"$concatArrays": ["$by_child", "$by_parent", ], }, }, },
            {"$project": {
                "by_parent": 0, "by_child": 0, }, },
        ]
        roles = self.collection.aggregate(pipeline=pipeline)
        return roles

    @parse_as(response_type=RoleResponse)
    def __get_permission_by_role_by_id(self, _id: str):
        pipeline = [
            {'$match': {'_id': ObjectId(_id)}},
            {'$lookup': {
                'from': 'permissions', 'localField': 'permission_ids', 'foreignField': '_id', 'as': 'by_parent'}},
            {'$lookup': {
                'from': 'permissions', 'localField': 'permission_ids', 'foreignField': 'sub_permissions._id',
                'as': 'by_child'}},
            {'$addFields': {
                'permissions': {'$concatArrays': ['$by_child', '$by_parent']}}},
            {'$project': {'by_parent': 0, 'by_child': 0}}
        ]

        result = self.collection.aggregate(pipeline=pipeline)
        return list(result)[0]

    def get_permission_by_role_by_id(self, _id: str):
        return self.__filter_permission(self.__get_permission_by_role_by_id(_id))

    def get_all_role(self, role_name: str = None):
        # result = [self.__filter_permission(role) for role in self.__get_all_role()]
        query = {}
        if role_name not in (None, ""):
            query["name"] = {"$regex": f".*{role_name}.*", "$options": "i"}
        result = self.collection.find(query)
        return result

    def count_role_usage(self, _id: str) -> int:
        pipeline = [
            {"$match": {"role_id": ObjectId(_id)}},
            {"$lookup": {
                "from": "accounts", "localField": "_id", "foreignField": "role_id", "as": "account", }, },
            {"$count": "count", },
        ]
        result = account_collection.aggregate(pipeline)
        result = list(result)
        return result[0]["count"] if result else 0

