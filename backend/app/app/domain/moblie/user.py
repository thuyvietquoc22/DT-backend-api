from typing import List

from app.decorator.parser import parse_cursor_as
from app.models.mobile.user import UserResponse
from app.models.pagination_model import Pageable
from app.repository.mobile.user import UserRepository


class UserDomain:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    @parse_cursor_as(response_type=List[UserResponse])
    def get_user(self, email: str, fullname: str, pageable: Pageable):
        return self.user_repo.get_users_by_fullname_email(fullname, email, pageable)


user_domain = UserDomain(UserRepository())
