from app.db.mongo.mongo_db import digital_twin_db

group_assets_collection = digital_twin_db.get_collection("group-assets")
group_assets_collection.create_index('keyname', unique=True)
