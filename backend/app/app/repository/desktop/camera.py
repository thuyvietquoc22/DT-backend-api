from bson import ObjectId
from pymongo.collection import Collection

from app.db.mongo_db import camera_collection, controller_collection
from app.decorator.parser import parse_as
from app.models.desktop.camera import CameraResponse, CameraCreate, CameraUpdate
from app.models.desktop.control.camera import CameraControl
from app.repository.base_repository import BaseRepository


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
            {'$unwind': '$model'}, {'$addFields': {'location': '$model.location'}},
            {'$project': {'model': 0}}
        ]

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


camera_repo = CameraRepository()
