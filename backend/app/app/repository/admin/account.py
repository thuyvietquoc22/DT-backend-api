from pymongo.collection import Collection
from pymongo.cursor import Cursor

from app.db.mongo_db import account_collection
from app.models.admin.account import AccountResponse, AccountUpdate, AccountCreate
from app.repository.base_repository import BaseRepository


class AccountRepository(BaseRepository[AccountResponse, AccountCreate, AccountUpdate]):

    @property
    def collection(self) -> Collection:
        return account_collection

    def find_by_username(self, username) -> Cursor:
        return self.collection.find_one({"username": username})

    def find_by_email(self, email):
        return self.collection.find_one({"email": email})
