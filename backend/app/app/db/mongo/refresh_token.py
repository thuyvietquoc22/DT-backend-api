from app.db.mongo.mongo_db import digital_twin_db

refresh_token_collection = digital_twin_db.get_collection("refresh-token")
