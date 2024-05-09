from bson import ObjectId
from pymongo.collection import Collection

from app.db.mongo.vms_sign import vms_sign_collection
from app.decorator.parser import parse_as
from app.models.desktop.vms_sign import VMSSignResponse, VMSSignUpdate, VMSSignCreate
from app.repository.base_repository import BaseRepository


class VMSSignRepository(BaseRepository[VMSSignResponse, VMSSignCreate, VMSSignUpdate]):

    @property
    def collection(self) -> Collection:
        return vms_sign_collection

    @property
    def pipeline_has_location(self):
        return [
            {'$lookup': {'from': 'model', 'localField': 'id_model', 'foreignField': '_id', 'as': 'model'}},
            {'$unwind': '$model'}, {'$addFields': {'location': '$model.location'}},
            {'$project': {'model': 0}}
        ]

    @parse_as(list[VMSSignResponse])
    def get_all_vms_sign(self):
        return self.collection.aggregate(self.pipeline_has_location)

    @parse_as(VMSSignResponse, get_first=True)
    def get_vms_sign_by_id(self, vms_sign_id):
        pipeline = [{'$match': {'_id': ObjectId(vms_sign_id)}}] + self.pipeline_has_location
        return self.collection.aggregate(pipeline)

    def get_vms_sign_inside_bound(self, min_lat, max_lat, min_lng, max_lng):
        pipeline = self.pipeline_has_location + [
            {'$match': {'location.lat': {'$gte': min_lat, '$lte': max_lat},
                        'location.lng': {'$gte': min_lng, '$lte': max_lng}}}
        ]

        return self.collection.aggregate(pipeline)

    def get_vms_sign_by_model_id(self, model_id):
        pipeline = [{'$match': {'id_model': ObjectId(model_id)}}] + self.pipeline_has_location
        return self.collection.aggregate(pipeline)
