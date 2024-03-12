from fastapi import APIRouter

from app.domain.user.user import UserResponse
from app.services.user_service import user_service


class UserRouter:
    @property
    def router(self):
        api_router = APIRouter(prefix='/mobile/users', tags=['User'])

        @api_router.get("", response_model=list[UserResponse])
        async def get_user(page: int = 1, limit: int = 10, email=None, fullname=None):
            return user_service.get_user(page=page, limit=limit, email=email, fullname=fullname)

        return api_router


user_router = UserRouter()
