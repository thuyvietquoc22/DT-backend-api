from app.db.mongo.mongo_db import digital_twin_db

bus_routes_collection = digital_twin_db.get_collection("master-bus_routes")
