import motor.motor_asyncio

from app.core.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
db = client.get_database("digital-twin")
users_collection = db.get_collection("users")
