from app.db.mongo_db import user_collection
from app.utils.common import convert_cursor_to_list


class UserService:

    @staticmethod
    def get_user(email: str, fullname: str, page: int = 1, limit: int = 10):
        query = {}
        if email:
            query["email"] = email
        if fullname:
            query["fullname"] = fullname
        result = user_collection.find(query).limit(limit).skip((page - 1) * limit)

        return convert_cursor_to_list(result)


user_service: UserService = UserService()
