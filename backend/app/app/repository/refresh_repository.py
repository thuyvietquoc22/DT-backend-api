from pymongo.errors import DuplicateKeyError

from app.db.mongo_db import refresh_token_collection


class RefreshTokenRepository:

    @property
    def collection(self):
        return refresh_token_collection

    def save_refresh_key(self, username: str, refresh_token: str) -> bool:
        try:
            self.collection.insert_one({
                "_id": username,
                "refresh_token": refresh_token
            })
        except DuplicateKeyError as e:
            self.collection.update_one(
                {"_id": username},
                {"$set": {"refresh_token": refresh_token}}
            )

        return True


refresh_token_repository = RefreshTokenRepository()
