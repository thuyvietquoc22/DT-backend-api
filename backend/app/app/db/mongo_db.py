from pymongo import MongoClient
from sentry_sdk.integrations import pymongo

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

refresh_token_collection = __db.get_collection("refresh-token")

address_collection = __db.get_collection("master-address")

cross_road_collection = __db.get_collection("cross_road")

camera_collection = __db.get_collection("camera")

traffic_light_collection = __db.get_collection("traffic_light")

vms_sign_collection = __db.get_collection("vms_sign")

connection_source = __db.get_collection("master-connection-source")
connection_source.create_index('keyname', unique=True)

controller_collection = __db.get_collection("controller")
