from bson import ObjectId
from pymongo.collection import Collection

from app.db.mongo.cross_road import cross_road_collection
from app.db.mongo.traffic_light import traffic_light_collection
from app.decorator import signleton
from app.decorator.parser import parse_as
from app.models.cms.model import ModelResponse
from app.models.desktop.traffic_light import TrafficLightResponse, TrafficLightCreate, TrafficLightUpdate
from app.repository.base_repository import BaseRepository
from app.repository.cms.model import ModelRepository


@signleton.singleton
class TrafficLightRepository(BaseRepository[TrafficLightResponse, TrafficLightCreate, TrafficLightUpdate]):
    @property
    def collection(self) -> Collection:
        return traffic_light_collection

    @property
    def cross_road_collection(self) -> Collection:
        return cross_road_collection

    @property
    def pipeline_has_location(self):
        return [
            {'$lookup': {'from': 'model', 'localField': 'id_model', 'foreignField': '_id', 'as': 'model'}},
            {'$unwind': '$model'}, {'$addFields': {'location': '$model.location'}},
            {'$project': {'model': 0}}
        ]

    @parse_as(list[TrafficLightResponse])
    def get_all_traffic_light(self):
        return self.collection.aggregate(self.pipeline_has_location)

    @parse_as(TrafficLightResponse, get_first=True)
    def get_traffic_light_by_id(self, traffic_light_id):
        pipeline = [{'$match': {'_id': ObjectId(traffic_light_id)}}] + self.pipeline_has_location
        return self.collection.aggregate(pipeline)

    def get_traffic_light_inside_bound(self, min_lat, max_lat, min_lng, max_lng):
        pipeline = self.pipeline_has_location + [
            {'$match': {'location.lat': {'$gte': min_lat, '$lte': max_lat},
                        'location.lng': {'$gte': min_lng, '$lte': max_lng}}}
        ]
        return self.collection.aggregate(pipeline)

    @parse_as(TrafficLightResponse, get_first=True)
    def get_traffic_light_by_model_id(self, model_id):
        pipeline = self.pipeline_has_location + [{'$match': {'id_model': ObjectId(model_id)}}]
        return self.collection.aggregate(pipeline)

    @parse_as(list[ModelResponse])
    def get_traffic_light_by_cross_road_id(self, cross_road_id: str):
        pipeline = [
                       {'$match': {'_id': ObjectId(cross_road_id)}},
                       {'$unwind': '$traffic_light_ids'},
                       {'$project': {'_id': 0, 'traffic_light_ids': 1}},
                       {'$lookup': {'from': 'model', 'localField': 'traffic_light_ids', 'foreignField': '_id',
                                    'as': 'traffic_light_ids'}},
                       {'$unwind': '$traffic_light_ids'},
                       {'$replaceRoot': {'newRoot': '$traffic_light_ids'}}
                   ] + ModelRepository().root_pipeline

        return self.cross_road_collection.aggregate(pipeline)
