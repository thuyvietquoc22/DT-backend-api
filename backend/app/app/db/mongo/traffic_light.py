from app.db.mongo.mongo_db import digital_twin_db

traffic_light_collection = digital_twin_db.get_collection("traffic_light")
