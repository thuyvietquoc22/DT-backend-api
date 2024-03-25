from pymongo import MongoClient

from app.core.config import settings

client = MongoClient(settings.MONGODB_URL)

__db = client["digital-twin"]

account_collection = __db.get_collection("account")
user_collection = __db.get_collection("user")
permission_collection = __db.get_collection("permissions")
role_collection = __db.get_collection("role")
refresh_token_collection = __db.get_collection("refresh_token")