import motor.motor_asyncio
from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.MONGODB_URL)

db = client["digital-twin"]

account_collection = db.get_collection("account")
user_collection = db.get_collection("user")

