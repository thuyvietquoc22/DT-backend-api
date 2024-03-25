from abc import ABC, abstractmethod
from math import ceil
from typing import TypeVar, Generic, Optional

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.cursor import Cursor

from app.exceptions.not_found_exception import NotFoundException
from app.models import BaseMongoModel
from app.models.pagination_model import Pageable

Model = TypeVar("Model", bound=BaseMongoModel)
CreateModel = TypeVar("CreateModel", bound=BaseMongoModel)
UpdateModel = TypeVar("UpdateModel", bound=BaseMongoModel)


class BaseRepository(Generic[Model, CreateModel, UpdateModel], ABC):

    @property
    @abstractmethod
    def collection(self) -> Collection:
        pass

    def get_pageable(self, pageable: Pageable, query: Optional[dict] = None) -> Pageable:
        total_elements = self.collection.count_documents(query)
        total_pages = ceil(total_elements / pageable.limit)
        pageable.pages = total_pages
        pageable.items = total_elements
        return pageable

    def get_all(self):
        return self.collection.find()

    def get_by_id(self, obj_id: str):
        result = self.collection.find_one({"_id": ObjectId(obj_id)})
        if not result:
            raise NotFoundException(f"Not found item has id: {obj_id}")
        return result

    def create(self, obj: CreateModel) -> Cursor:
        inserted = self.collection.insert_one(obj.model_dump(by_alias=True, exclude=["id"]))
        return self.collection.find_one({"_id": inserted.inserted_id})

    def update(self, obj_id: str, obj: UpdateModel):
        return self.collection.update_one({"_id": obj_id}, {"$set": obj.model_dump(by_alias=True, exclude=["id"])})

    def delete(self, obj_id: str):
        return self.collection.delete_one({"_id": obj_id})
