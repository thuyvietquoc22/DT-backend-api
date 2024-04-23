from app.db.mongo.mongo_db import digital_twin_db

vms_sign_collection = digital_twin_db.get_collection("vms_sign")
