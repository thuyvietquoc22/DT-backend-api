from app.db.mongo.mongo_db import digital_twin_db

passage_capacity_status_collection = digital_twin_db.get_collection("master-passage_capacity_status")
passage_capacity_status_collection.create_index('keyname', unique=True)