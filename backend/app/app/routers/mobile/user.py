from fastapi import APIRouter

from app.domain.pagination_response import PaginationResponse as Pagination
from app.domain.user.user import UserResponse
from app.services.user_service import user_service


class UserRouter:
    @property
    def router(self):
        api_router = APIRouter(prefix='/mobile/users', tags=['User'])

        @api_router.get("", response_model=Pagination[UserResponse])
        async def get_user(page: int = 1, limit: int = 10, email=None, fullname=None):
            response, total_page, total_items = user_service.get_user(page=page, limit=limit, email=email,
                                                                      fullname=fullname)
            return Pagination.response(response, total_page, total_items, page, limit)

        return api_router


user_router = UserRouter()
