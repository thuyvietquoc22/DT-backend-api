from typing import List

from app.decorator.parser import parse_as
from app.exceptions.not_found_exception import NotFoundException
from app.models.mobile.user import UserResponse
from app.models.pagination_model import Pageable
from app.repository.mobile.user import UserRepository


class UserDomain:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    @parse_as(response_type=List[UserResponse])
    def get_user(self, email: str, fullname: str, pageable: Pageable):
        return self.user_repo.get_users_by_fullname_email(fullname, email, pageable)

    @parse_as(response_type=UserResponse)
    def lock_user(self, user_id):
        return self.user_repo.set_is_banned(user_id, True)

    @parse_as(response_type=UserResponse)
    def unlock_user(self, user_id):
        return self.user_repo.set_is_banned(user_id, False)


user_domain = UserDomain(UserRepository())
