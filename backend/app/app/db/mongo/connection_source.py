from app.db.mongo.mongo_db import digital_twin_db

connection_source = digital_twin_db.get_collection("master-connection-source")
connection_source.create_index('keyname', unique=True)
