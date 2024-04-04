from pymongo import MongoClient

from app.core.config import settings

client = MongoClient(settings.MONGODB_URL)

__db = client["digital-twin"]

account_collection = __db.get_collection("account")
user_collection = __db.get_collection("user")
permission_collection = __db.get_collection("permissions")
assets_collection = __db.get_collection("assets")
model_collection = __db.get_collection("model")
group_assets_collection = __db.get_collection("group-assets")
role_collection = __db.get_collection("role")
refresh_token_collection = __db.get_collection("refresh_token")
address_collection = __db.get_collection("address")
cross_road_collection = __db.get_collection("cross_road")
camera_collection = __db.get_collection("camera")