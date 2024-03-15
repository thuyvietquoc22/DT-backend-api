from fastapi import APIRouter

from app.domain.moblie.user import UserResponse, UserDomain
from app.models.pagination_model import PaginationResponse, Pageable


class UserRouter:

    def __init__(self, user_domain: UserDomain):
        self.user_domain = user_domain

    @property
    def router(self):
        api_router = APIRouter(prefix='/mobile/users', tags=['User'])

        @api_router.get("", response_model=PaginationResponse[UserResponse])
        async def get_user(page: int = 1, limit: int = 10, email=None, fullname=None):
            pageable = Pageable(page=page, limit=limit)
            response = self.user_domain.get_user(pageable=pageable, email=email, fullname=fullname)

            return PaginationResponse.response_pageable(data=response, pageable=pageable)

        return api_router
