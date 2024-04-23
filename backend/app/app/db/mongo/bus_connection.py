from app.db.mongo.mongo_db import digital_twin_db

bus_connection_collection = digital_twin_db.get_collection("master-bus_connection")
bus_connection_collection.create_index('code', unique=True)
