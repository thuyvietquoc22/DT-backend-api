from bson import ObjectId
from pymongo.collection import Collection

from app.db.mongo_db import cross_road_collection
from app.decorator.parser import parse_as
from app.models.desktop.master_data.cross_road import CrossRoadResponse, CrossRoadCreate, CrossRoadUpdate
from app.models.pagination_model import Pageable
from app.repository.base_repository import BaseRepository


class CrossRoadRepo(BaseRepository[CrossRoadResponse, CrossRoadCreate, CrossRoadUpdate]):

    @property
    def collection(self) -> Collection:
        return cross_road_collection

    @property
    def pipeline_has_address(self):
        return [
            {'$lookup': {'from': 'master-address', 'localField': 'province_code', 'foreignField': 'code',
                         'as': 'province'}},
            {'$addFields': {'province': {'$arrayElemAt': ['$province', 0]}}},
            {'$unwind': '$province.districts'},
            {'$match': {'$expr': {'$eq': ['$province.districts.code', '$district_code']}}},
            {'$addFields': {'district': '$province.districts'}},
            {'$project': {'district.wards': 0, 'province.districts': 0}}
        ]

    def check_district_code(self, district_code):
        pass

    @parse_as(response_type=list[CrossRoadResponse])
    def find_all_cross_road(self, pageable: Pageable):
        pipeline = pageable.pipeline + self.pipeline_has_address
        self.get_pageable(pageable)
        return self.collection.aggregate(pipeline)

    @parse_as(response_type=list[CrossRoadResponse])
    def find_cross_road_by_district_id(self, district_id, pageable: Pageable):
        query = {'district_code': district_id}
        pipeline = [{'$match': query}] + self.pipeline_has_address + pageable.pipeline
        self.get_pageable(pageable, query)
        return self.collection.aggregate(pipeline)

    @parse_as(response_type=CrossRoadResponse, get_first=True)
    def get_cross_road_by_id(self, cross_road_id):
        pipeline = [
                       {'$match': {'_id': ObjectId(cross_road_id)}}
                   ] + self.pipeline_has_address

        return self.collection.aggregate(pipeline)


cross_road_repo = CrossRoadRepo()
