from bson import ObjectId
from pymongo.collection import Collection

from app.db.mongo.model import model_collection
from app.decorator.parser import parse_as
from app.models.cms.assets import GroupAssets
from app.models.cms.model import ModelUpdate, ModelCreate, ModelResponse, Location
from app.models.pagination_model import Pageable
from app.repository.base_repository import BaseRepository


class ModelRepository(BaseRepository[ModelResponse, ModelCreate, ModelUpdate]):
    @property
    def collection(self) -> Collection:
        return model_collection

    @property
    def root_pipeline(self):
        return [
            {'$lookup': {'from': 'assets', 'localField': 'asset_id', 'foreignField': '_id', 'as': 'resultArray'}},
            {'$addFields': {'asset': {'$arrayElemAt': ['$resultArray', 0]}}},
            {'$lookup': {'from': 'group-assets', 'localField': 'asset.group_id', 'foreignField': 'keyname',
                         'as': 'asset.group'}},
            {'$addFields': {'asset.group': {'$arrayElemAt': ['$asset.group', 0]}}},
            {'$project': {'resultArray': 0, 'asset_id': 0}},
            {'$lookup': {'from': 'camera', 'localField': '_id', 'foreignField': 'id_model', 'as': 'cam'}},
            {'$lookup': {'from': 'vms_sign', 'localField': '_id', 'foreignField': 'id_model', 'as': 'vms'}},
            {'$addFields': {'connector': {'$concatArrays': ['$vms', '$cam']}}},
            {'$addFields': {'connected': {'$gt': [{'$size': {'$ifNull': ['$connector', []]}}, 0]}}}
        ]

    @parse_as(ModelResponse)
    def save(self, obj: ModelCreate):
        inserted = self.collection.insert_one(obj.model_dump(by_alias=True, exclude={"id"})).inserted_id

        return self.collection.aggregate(self.root_pipeline)

    def get_by_id(self, obj_id: str):
        pipeline = self.root_pipeline + [
            {'$match': {'_id': ObjectId(obj_id)}}
        ]

        return self.collection.aggregate(pipeline)

    #
    def get_models(self, pageable):
        pipeline = self.root_pipeline + [
            {'$skip': pageable.skip},
            {'$limit': pageable.limit}
        ]

        return self.collection.aggregate(pipeline)

    def get_by_area(self, start: Location, end: Location, limit):
        start = start.to_array()
        end = end.to_array()
        pipeline = self.root_pipeline + [
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
            {'$lookup': {'from': 'group-assets', 'localField': 'asset.group_id', 'foreignField': 'keyname',
                         'as': 'group'}},
            {'$unwind': '$group'},
            {'$replaceRoot': {'newRoot': '$group'}}
        ]

        return self.collection.aggregate(pipeline)

    @parse_as(list[ModelResponse])
    def get_bus_stop(self):
        """
        Get list model has asset type keyname is "BUS_STOP"
        """
        pipeline = self.root_pipeline + [
            {'$match': {'asset.group_id': 'BUS_STOP'}}
        ]
        return self.collection.aggregate(pipeline)

    @parse_as(list[ModelResponse])
    def get_models_by_group(self, group: list[str], pageable: Pageable):
        query = {'asset.group_id': {'$in': group}}
        pipeline = self.root_pipeline + [
            {'$match': query},
            {'$skip': pageable.skip},
            {'$limit': pageable.limit}
        ]

        self.get_pageable(pageable, query)
        return self.collection.aggregate(pipeline)

    @parse_as(list[ModelResponse])
    def get_list_models_by_ids(self, model_ids: list[str]):
        query = {'_id': {'$in': [ObjectId(id_) for id_ in model_ids]}}
        pipeline = self.root_pipeline + [
            {'$match': query}
        ]

        return self.collection.aggregate(pipeline)

    @parse_as(list[ModelResponse])
    def find_models_by_ids_and_group(self, traffic_light_id, group_key):
        pipeline = self.root_pipeline + [
            {'$match': {'asset.group_id': group_key, '_id': {'$in': [ObjectId(id_) for id_ in traffic_light_id]}}}
        ]
        return self.collection.aggregate(pipeline)
