from pymongo import MongoClient
from sentry_sdk.integrations import pymongo

from app.core.config import settings

client = MongoClient(settings.MONGODB_URL)

__db = client["digital-twin"]


def start_session():
    return client.start_session()


"""
COLLECTIONS
"""

account_collection = __db.get_collection("account")

user_collection = __db.get_collection("user")

permission_collection = __db.get_collection("permissions")

assets_collection = __db.get_collection("assets")

model_collection = __db.get_collection("model")

group_assets_collection = __db.get_collection("group-assets")
group_assets_collection.create_index('keyname', unique=True)

role_collection = __db.get_collection("role")

refresh_token_collection = __db.get_collection("refresh-token")

address_collection = __db.get_collection("master-address")

cross_road_collection = __db.get_collection("master-cross_road")

camera_collection = __db.get_collection("camera")

traffic_light_collection = __db.get_collection("traffic_light")

vms_sign_collection = __db.get_collection("vms_sign")

connection_source = __db.get_collection("master-connection-source")
connection_source.create_index('keyname', unique=True)

controller_collection = __db.get_collection("controller")

vms_component_collection = __db.get_collection("master-vms_component")

street_collection = __db.get_collection("master-street")

traffic_data_collection = __db.get_collection("traffic_data")

vehicle_type_collection = __db.get_collection("master-vehicle_type")
vehicle_type_collection.create_index('type', unique=True)

passage_capacity_status_collection = __db.get_collection("master-passage_capacity_status")
passage_capacity_status_collection.create_index('keyname', unique=True)

bus_routes_collection = __db.get_collection("master-bus_routes")

bus_connection_collection = __db.get_collection("master-bus_connection")
bus_connection_collection.create_index('code', unique=True)
