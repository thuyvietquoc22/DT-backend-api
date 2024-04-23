from app.db.mongo.mongo_db import digital_twin_db

vehicle_type_collection = digital_twin_db.get_collection("master-vehicle_type")
vehicle_type_collection.create_index('type', unique=True)