from app.db.mongo.mongo_db import digital_twin_db

camera_collection = digital_twin_db.get_collection("camera")
camera_collection.create_index("id_model", unique=True)
camera_collection.create_index("camera_code", unique=True)
