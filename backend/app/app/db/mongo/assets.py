from app.db.mongo.mongo_db import digital_twin_db

assets_collection = digital_twin_db.get_collection("assets")
