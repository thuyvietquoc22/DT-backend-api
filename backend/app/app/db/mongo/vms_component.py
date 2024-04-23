from app.db.mongo.mongo_db import digital_twin_db

vms_component_collection = digital_twin_db.get_collection("master-vms_component")
