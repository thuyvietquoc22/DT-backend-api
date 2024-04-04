from abc import ABC, abstractmethod
from math import ceil
from typing import TypeVar, Generic, Optional

from bson import ObjectId
from pydantic import BaseModel
from pymongo.collection import Collection
from pymongo.cursor import Cursor

from app.models import BaseMongoModel
from app.models.pagination_model import Pageable

Model = TypeVar("Model", bound=BaseMongoModel)
CreateModel = TypeVar("CreateModel", bound=BaseMongoModel)
UpdateModel = TypeVar("UpdateModel", bound=BaseModel)


class BaseRepository(Generic[Model, CreateModel, UpdateModel], ABC):

    @property
    @abstractmethod
    def collection(self) -> Collection:
        pass

    def is_exists_id(self, id_: str) -> bool:
        id_ = ObjectId(id_)
        return self.collection.count_documents({"_id": id_}) > 0

    def is_exists_ids(self, ids: list[str]) -> bool:
        ids = [ObjectId(id_) for id_ in ids]
        return self.collection.count_documents({"_id": {"$in": ids}}) == len(ids)

    def get_pageable(self, pageable: Pageable, query: Optional[dict] = None) -> Pageable:
        total_elements = self.collection.count_documents(query or {})
        total_pages = ceil(total_elements / pageable.limit)
        pageable.pages = total_pages
        pageable.items = total_elements
        return pageable

    def find_by_ids(self, ids: list[str], pageable: Pageable = None):
        ids = [ObjectId(id_) for id_ in ids]
        if pageable:
            self.get_pageable(pageable, {"_id": {"$in": ids}})
            return self.collection.find({"_id": {"$in": ids}}).skip(pageable.skip).limit(pageable.limit)
        else:
            return self.collection.find({"_id": {"$in": ids}})

    def get_all(self, pageable: Pageable = None) -> Cursor:
        if pageable:
            self.get_pageable(pageable)
            return self.collection.find().skip(pageable.skip).limit(pageable.limit)
        else:
            return self.collection.find()

    def get_by_id(self, obj_id: str) -> Optional[Model]:
        return self.collection.find_one({"_id": ObjectId(obj_id)})

    def create(self, obj: CreateModel) -> Cursor:
        inserted = self.collection.insert_one(obj.model_dump(by_alias=True, exclude={"id"}))
        return self.collection.find_one({"_id": inserted.inserted_id})

    def update(self, obj_id: str, obj: UpdateModel):
        if hasattr(obj, "_id"):
            obj._id = None

        # remove attr is None of obj
        obj = obj.dict(exclude_none=True)

        result = self.collection.update_one({"_id": ObjectId(obj_id)}, {"$set": obj})

        if result.modified_count == 0:
            raise Exception("Không có bản ghi nào được cập nhật")

        return result

    def delete(self, obj_id: str):
        return self.collection.delete_one({"_id": ObjectId(obj_id)})
