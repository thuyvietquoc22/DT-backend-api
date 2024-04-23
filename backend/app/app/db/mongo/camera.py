from app.db.mongo.mongo_db import digital_twin_db

camera_collection = digital_twin_db.get_collection("camera")
