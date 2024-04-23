from app.db.mongo.mongo_db import digital_twin_db

permission_collection = digital_twin_db.get_collection("permissions")
