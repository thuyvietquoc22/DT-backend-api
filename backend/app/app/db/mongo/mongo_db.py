from pymongo import MongoClient

from app.core.config import settings

client = MongoClient(settings.MONGODB_URL)

digital_twin_db = client["digital-twin"]


def start_session():
    return client.start_session()
