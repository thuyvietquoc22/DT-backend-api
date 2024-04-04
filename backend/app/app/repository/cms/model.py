from bson import ObjectId
from pymongo.collection import Collection

from app.db.mongo_db import model_collection
from app.decorator.parser import parse_as
from app.models.cms.assets import GroupAssets
from app.models.cms.model import ModelUpdate, ModelCreate, ModelResponse, Location
from app.repository.base_repository import BaseRepository


class ModelRepository(BaseRepository[ModelResponse, ModelCreate, ModelUpdate]):
    @property
    def collection(self) -> Collection:
        return model_collection

    @property
    def pipeline(self):
        return [
            {'$lookup': {'from': 'assets', 'localField': 'asset_id', 'foreignField': '_id', 'as': 'resultArray'}},
            {'$addFields': {'asset': {'$arrayElemAt': ['$resultArray', 0]}}},
            {'$lookup': {'from': 'group-assets', 'localField': 'asset.group_id', 'foreignField': '_id',
                         'as': 'asset.group'}},
            {'$addFields': {'asset.group': {'$arrayElemAt': ['$asset.group', 0]}}},
            {'$project': {'resultArray': 0, 'asset_id': 0}}]

    @parse_as(ModelResponse)
    def save(self, obj: ModelCreate):
        inserted = self.collection.insert_one(obj.model_dump(by_alias=True, exclude=["id"])).inserted_id

        return self.collection.aggregate(self.pipeline)

    def get_by_id(self, obj_id: str):
        pipeline = self.pipeline + [
            {'$match': {'_id': ObjectId(obj_id)}}
        ]

        return self.collection.aggregate(pipeline)

    #
    def get_models(self, pageable):
        pipeline = self.pipeline + [
            {'$skip': pageable.skip},
            {'$limit': pageable.limit}
        ]

        return self.collection.aggregate(pipeline)

    def get_by_area(self, start: Location, end: Location, limit):
        start = start.to_array()
        end = end.to_array()
        pipeline = self.pipeline + [
            {'$match': {'location': {'$geoWithin': {'$box': [start, end]}}}},
            {'$limit': limit}
        ]

        return self.collection.aggregate(pipeline)

    def delete_by_asset_id(self, asset_id):
        return self.collection.delete_many({"asset_id": ObjectId(asset_id)})

    @parse_as(GroupAssets, True)
    def get_group_by_model_id(self, model_id):
        pipeline = [
            {'$match': {'_id': ObjectId(model_id)}},
            {'$lookup': {'from': 'assets', 'localField': 'asset_id', 'foreignField': '_id', 'as': 'asset'}},
            {'$unwind': '$asset'},
            {'$lookup': {'from': 'group-assets', 'localField': 'asset.group_id', 'foreignField': '_id', 'as': 'group'}},
            {'$unwind': '$group'},
            {'$replaceRoot': {'newRoot': '$group'}}
        ]

        return self.collection.aggregate(pipeline)
