from bson import ObjectId
from pymongo.collection import Collection
from pymongo.cursor import Cursor

from app.db.mongo.account import account_collection
from app.decorator.parser import parse_as
from app.models.cms.account import AccountResponse, AccountUpdate, AccountCreate, AccountModel
from app.models.pagination_model import Pageable
from app.repository.base_repository import BaseRepository


class AccountRepository(BaseRepository[AccountResponse, AccountCreate, AccountUpdate]):

    @property
    def collection(self) -> Collection:
        return account_collection

    def find_by_username(self, username) -> Cursor:
        return self.collection.find_one({"username": username})

    @parse_as(response_type=AccountModel)
    def find_by_email(self, email):
        result = self.collection.find_one({"email": email})
        return result

    def update_first_login(self, _id: str, hash_password: str):
        return self.collection.update_one({"_id": ObjectId(_id)},
                                          {"$set": {"password": hash_password, "first_login": False}})

    @parse_as(response_type=list[AccountResponse])
    def find_all(self, pageable: Pageable, name: str, email: str):
        query = {}
        if email:
            query["email"] = {"$regex": f".*{email}.*", "$options": "i"}
        if name:
            query["fullname"] = {"$regex": f".*{name}.*", "$options": "i"}
        pipeline = [
            {'$match': query},
            {'$lookup': {'from': 'role', 'localField': 'role_id', 'foreignField': '_id', 'as': 'role_name'}},
            {'$addFields': {'role_name': {'$arrayElemAt': ['$role_name.name', 0]}}},
            {"$skip": pageable.skip},
            {"$limit": pageable.limit}
        ]

        self.get_pageable(pageable, query)
        result = self.collection.aggregate(pipeline)
        return result

    @parse_as(response_type=list[AccountResponse])
    def get_account_by_id(self, _id):
        pipeline = [
            {'$match': {"_id": ObjectId(_id)}},
            {'$lookup': {'from': 'role', 'localField': 'role_id', 'foreignField': '_id', 'as': 'role_name'}},
            {'$addFields': {'role_name': {'$arrayElemAt': ['$role_name.name', 0]}}}
        ]
        result = self.collection.aggregate(pipeline)
        return result

    def update_password_by_id(self, _id, hashed):
        result = self.collection.update_one({"_id": ObjectId(_id)}, {"$set": {"password": hashed}})
        return result.modified_count == 1

