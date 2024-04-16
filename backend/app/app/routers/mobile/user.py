from fastapi import APIRouter

from app.routers import MobileTag, BaseRouter
from app.sevices.moblie.user import UserResponse, UserService
from app.models.pagination_model import PaginationResponse, Pageable


class UserRouter(BaseRouter):

    def __init__(self):
        self.user_service = UserService()

    @property
    def router(self):
        api_router = APIRouter(prefix='/mobile/users', tags=MobileTag().get(name="Users", is_mater_data=False))

        @api_router.get("", response_model=PaginationResponse[UserResponse])
        async def get_user(page: int = 1, limit: int = 10, email=None, fullname=None):
            pageable = Pageable(page=page, limit=limit)
            response = self.user_service.get_user(pageable=pageable, email=email, fullname=fullname)

            return PaginationResponse.response_pageable(data=response, pageable=pageable)

        @api_router.patch("/lock/{user_id}", response_model=UserResponse)
        async def lock_user(user_id: str):
            response = self.user_service.lock_user(user_id=user_id)
            return response

        @api_router.patch("/unlock/{user_id}", response_model=UserResponse)
        async def unlock_user(user_id: str):
            response = self.user_service.unlock_user(user_id=user_id)
            return response

        return api_router
