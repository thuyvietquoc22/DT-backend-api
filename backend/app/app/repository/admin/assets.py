from bson import ObjectId
from pymongo.collection import Collection

from app.db.mongo_db import assets_collection, group_assets_collection, model_collection
from app.decorator.parser import parse_as
from app.models.admin.assets import AssetsResponse, AssetsCreate, AssetsUpdate, GroupAssets
from app.repository.base_repository import BaseRepository


class AssetsModelRepository(BaseRepository[AssetsResponse, AssetsCreate, AssetsUpdate]):
    @property
    def collection(self) -> Collection:
        return assets_collection

    @property
    def group_assets_collection(self) -> Collection:
        return group_assets_collection

    @property
    def pipeline(self):
        return [
            {'$lookup': {'from': 'group-assets', 'localField': 'group_id', 'foreignField': '_id', 'as': 'group'}},
            {'$addFields': {'group': {'$arrayElemAt': ['$group', 0]}}},
            {'$project': {'group_id': 0}}
        ]

    def update_name(self, asset_id, name):
        return self.collection.update_one({"_id": ObjectId(asset_id)}, {"$set": {"name": name}})

    def get_all_name(self):
        pipeline = [
            {'$group': {'_id': '$name'}},
            {'$project': {'_id': 0, 'name': '$_id'}}
        ]
        return self.collection.aggregate(pipeline)

    @parse_as(list[GroupAssets])
    def get_all_group(self):
        return self.group_assets_collection.find({})

    def update_url(self, asset_id, object_3d: str = None, texture: str = None, image: str = None):
        update_data = {}
        if object_3d:
            update_data['object_3d'] = object_3d
        if texture:
            update_data['texture'] = texture
        if image:
            update_data['image'] = image
        return self.collection.update_one({"_id": ObjectId(asset_id)}, {"$set": update_data})

    def get_group_by_id(self, group_id):
        return self.group_assets_collection.find_one({"_id": ObjectId(group_id)})

    #
    def get_all_assets(self, pageable):
        self.get_pageable(pageable)
        pipeline = self.pipeline + [{'$skip': pageable.skip}, {'$limit': pageable.limit}]
        return self.collection.aggregate(pipeline)

    def get_assets_by_ids(self, _ids: list[str]):
        ids = [ObjectId(id_) for id_ in _ids]
        pipeline = self.pipeline + [{'$match': {'_id': {'$in': ids}}}]
        return self.collection.aggregate(pipeline)

    def create_asset(self, model: AssetsCreate):
        id_inserted = self.collection.insert_one(model.dict(by_alias=True, exclude={"id"})).inserted_id
        pipeline = self.pipeline + [{'$match': {'_id': id_inserted}}]
        return self.collection.aggregate(pipeline)

    def find_by_public_id(self, public_id):
        pipeline = self.pipeline + [{'$match': {'public_id': public_id}}]
        return self.collection.aggregate(pipeline)

    @staticmethod
    def count_usage(asset_id):
        return model_collection.count_documents({"asset_id": ObjectId(asset_id)})







