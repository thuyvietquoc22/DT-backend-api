from app.db.mongo.mongo_db import digital_twin_db

traffic_data_collection = digital_twin_db.get_collection("traffic_data")
