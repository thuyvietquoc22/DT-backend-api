from app.db.mongo.mongo_db import digital_twin_db

cross_road_collection = digital_twin_db.get_collection("master-cross_road")
