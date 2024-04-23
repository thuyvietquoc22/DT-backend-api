from app.db.mongo.mongo_db import digital_twin_db

cross_road_collection = digital_twin_db.get_collection("master-cross_road")
cross_road_collection.create_index('street_ids', unique=True)
