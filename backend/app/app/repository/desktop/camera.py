from bson import ObjectId
from pymongo.collection import Collection

from app.db.mongo.controller import controller_collection
from app.db.mongo.camera import camera_collection
from app.decorator import signleton
from app.decorator.parser import parse_as
from app.models.desktop.camera import CameraResponse, CameraCreate, CameraUpdate, CameraTrafficDataResponse
from app.repository.base_repository import BaseRepository


@signleton.singleton
class CameraRepository(BaseRepository[CameraResponse, CameraCreate, CameraUpdate]):
    @property
    def collection(self) -> Collection:
        return camera_collection

    @property
    def control_collection(self) -> Collection:
        return controller_collection

    @property
    def pipeline_has_location(self):
        return [
            {'$lookup': {'from': 'model', 'localField': 'id_model', 'foreignField': '_id', 'as': 'model'}},
            {'$unwind': '$model'},
            {'$lookup': {'from': 'master-street', 'localField': 'street_id', 'foreignField': '_id', 'as': 'street'}},
            {'$unwind': '$street'},
            {'$addFields': {'location': '$model.location'}},
            {'$project': {'model': 0, 'street_id': 0}},

        ]

    @property
    def root_pipeline(self):
        return self.pipeline_has_location

    @parse_as(response_type=list[CameraResponse])
    def get_all_camera(self):
        return self.collection.aggregate(self.pipeline_has_location)

    @parse_as(response_type=CameraResponse, get_first=True)
    def get_camera_by_id(self, camera_id):
        pipeline = [{'$match': {'_id': ObjectId(camera_id)}}] + self.pipeline_has_location
        return self.collection.aggregate(pipeline)

    @parse_as(response_type=list[CameraResponse])
    def get_camera_inside_bound(self, min_lat, max_lat, min_lng, max_lng):
        pipeline = self.pipeline_has_location + [
            {'$match': {
                'location.lat': {'$gte': min_lat, '$lte': max_lat},
                'location.lng': {'$gte': min_lng, '$lte': max_lng}
            }}
        ]

        return self.collection.aggregate(pipeline)

    @parse_as(response_type=list[CameraTrafficDataResponse])
    def get_last_data_camera_inside_bound(self, min_lat, max_lat, min_lng, max_lng, minute_ago):
        # Get location
        pipeline = self.pipeline_has_location

        # Filter
        pipeline += [{
            '$match': {
                'location.lat': {'$gte': min_lat, '$lte': max_lat},
                'location.lng': {'$gte': min_lng, '$lte': max_lng}
            }
        }]

        #  Get street
        # pipeline += [
        #     {'$lookup': {'from': 'master-street', 'localField': 'street_id', 'foreignField': '_id', 'as': 'street'}},
        #     {'$unwind': '$street'}
        # ]

        pipeline += [
            {'$lookup': {
                'from': 'traffic_data',
                'let': {'camera_id': '$_id'},
                'pipeline': [
                    {'$match': {'$expr': {'$eq': ['$camera_id', '$$camera_id']}}},
                    {'$sort': {'time': -1}},
                    {'$limit': 1}],
                'as': 'live_passage_capacity'
            }}
        ]

        return self.collection.aggregate(pipeline)

    @parse_as(response_type=CameraResponse, get_first=True)
    def get_camera_by_model_id(self, model_id):
        pipeline = self.pipeline_has_location + [{'$match': {'id_model': ObjectId(model_id)}}]
        return self.collection.aggregate(pipeline)

    def get_camera_by_code(self, camera_code):
        pass
