from pymongo.collection import Collection

from app.db.mongo_db import user_collection
from app.models.mobile.user import UserModelCreate
from app.models.pagination_model import Pageable
from app.repository.base_repository import BaseRepository


class UserRepository(BaseRepository[UserModelCreate, UserModelCreate, UserModelCreate]):
    @property
    def collection(self) -> Collection:
        return user_collection

    def find_by_username(self, username):
        return self.collection.find_one({"username": username})

    def find_by_email(self, email):
        return self.collection.find_one({"email": email})

    def get_users_by_fullname_email(self, fullname, email, pageable: Pageable):
        query = {}
        if email:
            query["email"] = {"$regex": f".*{email}.*", "$options": "i"}
        if fullname:
            query["fullname"] = {"$regex": f".*{fullname}.*", "$options": "i"}

        self.get_pageable(pageable, query)

        result = self.collection.find(query).skip(pageable.skip).limit(pageable.limit)

        return result
