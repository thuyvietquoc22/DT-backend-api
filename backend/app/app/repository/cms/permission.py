from bson import ObjectId
from pymongo.collection import Collection

from app.db.mongo.permission import permission_collection
from app.decorator.parser import parse_as
from app.models.cms.permission import PermissionResponse


class PermissionRepository:

    @property
    def collection(self) -> Collection:
        return permission_collection

    def get_all(self):
        return self.collection.find({})

    @parse_as(response_type=list[PermissionResponse])
    def get_permission_by_id(self, permission_ids: list[str]):
        ids = [ObjectId(permission_id) for permission_id in permission_ids]

        pipeline = [
            {'$addFields': {'sub_permissions': {'$concatArrays': ['$sub_permissions', ['$$ROOT']]}}},
            {'$unwind': '$sub_permissions'},
            {'$addFields': {'_id': '$sub_permissions._id', 'name': '$sub_permissions.name'}},
            {'$project': {'sub_permissions': 0}},
            {'$match': {'_id': {'$in': ids}}},
        ]
        return self.collection.aggregate(pipeline)
