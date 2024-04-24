from app.db.mongo.mongo_db import digital_twin_db

vms_component_category_collection = digital_twin_db.get_collection("master-vms_component_category")
vms_component_category_collection.create_index("keyname", unique=True)
