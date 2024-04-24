from pymongo.collection import Collection

from app.db.mongo.vms_component_category import vms_component_category_collection
from app.decorator.parser import parse_as
from app.models.desktop.master_data.vms_component_category import VMSComponentCategoryResponse
from app.models.pagination_model import Pageable
from app.repository.base_repository import BaseRepository


class VMSComponentCategoryRepository(BaseRepository):
    @property
    def collection(self) -> Collection:
        return vms_component_category_collection

    @parse_as(list[VMSComponentCategoryResponse])
    def get_all(self, pageable: Pageable = None):
        return super().get_all(pageable)

    def check_keyname_exist(self, keyname):
        return self.collection.find_one({"keyname": keyname}) is not None

    @parse_as(list[VMSComponentCategoryResponse])
    def get_all_by_type(self, component_type):
        pipeline = [
            {"$match": {"type": component_type}}
        ]
        return self.collection.aggregate(pipeline)
