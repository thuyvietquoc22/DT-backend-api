from bson import ObjectId
from pymongo.collection import Collection

from app.db.mongo.vms_component import vms_component_collection
from app.decorator import signleton
from app.decorator.parser import parse_as
from app.models.desktop.master_data.vms_component import VMSComponentCreate, VMSComponentUpdate, VMSComponentResponse
from app.repository.base_repository import BaseRepository


@signleton.singleton
class VMSComponentRepository(BaseRepository[VMSComponentResponse, VMSComponentCreate, VMSComponentUpdate]):
    @property
    def collection(self) -> Collection:
        return vms_component_collection

    @property
    def root_pipeline(self):
        return [
            {'$lookup': {'from': 'master-vms_component_category', 'localField': 'category_key',
                         'foreignField': 'keyname', 'as': 'category'}},
            {'$unwind': {'path': '$category', 'preserveNullAndEmptyArrays': True}}
        ]

    @parse_as(response_type=VMSComponentResponse, get_first=True)
    def get_vms_component_by_code(self, code):
        return self.collection.aggregate([{"$match": {"code": code}}] + self.root_pipeline)

    @parse_as(response_type=VMSComponentResponse, get_first=True)
    def get_vms_component_by_code_type(self, code, type_):
        return self.collection.aggregate([{"$match": {"code": code, "type": type_}}] + self.root_pipeline)

    @parse_as(response_type=list[VMSComponentResponse])
    def get_all_vms_component(self):
        return self.collection.aggregate(self.root_pipeline)

    @parse_as(VMSComponentResponse, True)
    def get_vms_component_by_id(self, vms_component_id):
        # return self.collection.find_one({"_id": ObjectId(vms_component_id)})
        pipeline = [
                       {"$match": {"_id": ObjectId(vms_component_id)}}
                   ] + self.root_pipeline
        return self.collection.aggregate(pipeline)

    def update_url_vms_component_by_id(self, vms_component_id, url):
        self.collection.update_one({"_id": ObjectId(vms_component_id)}, {"$set": {"url": url}})

    @parse_as(response_type=list[VMSComponentResponse])
    def get_by_ids(self, ids: list[str]):
        query = {"_id": {"$in": [ObjectId(id_) for id_ in ids]}}
        pipeline = [
                       {"$match": query}
                   ] + self.root_pipeline

        return self.collection.aggregate(pipeline)

    @parse_as(response_type=list[VMSComponentResponse])
    def get_vms_component_by_type(self, tag_name):
        pipeline = [
                       {"$match": {"type": tag_name}}
                   ] + self.root_pipeline
        return self.collection.aggregate(pipeline)
