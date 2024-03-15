from pymongo.collection import Collection


class PermissionRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def get_all(self):
        return self.collection.find()
