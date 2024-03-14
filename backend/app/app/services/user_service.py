from math import ceil

from app.db.mongo_db import user_collection
from app.domain.user.user import UserResponse
from app.models.user_model import UserModel
from app.utils.common import convert_cursor_to_list


class UserService:

    @staticmethod
    def get_user(email: str, fullname: str, page: int = 1, limit: int = 10) -> tuple[list[UserResponse], int, int]:
        query = {}
        if email:
            query["email"] = {"$regex": f".*{email}.*", "$options": "i"}
        if fullname:
            query["fullname"] = {"$regex": f".*{fullname}.*", "$options": "i"}

        total_elements = user_collection.count_documents(query)
        total_pages = ceil(total_elements / limit)

        result = user_collection.find(query).limit(limit).skip((page - 1) * limit)

        return convert_cursor_to_list(result, data_type=UserResponse), total_pages, total_elements


user_service: UserService = UserService()
