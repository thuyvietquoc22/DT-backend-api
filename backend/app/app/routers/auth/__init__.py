from typing import List

from fastapi import APIRouter
from fastapi import HTTPException



class UsersRouter:
    def __init__(self ) -> None:
        self.users_domain = True

    @property
    def router(self):
        api_router = APIRouter(prefix='/auth', tags=['Auth'])

        @api_router.post('/login')
        def create_user():
            return self.users_domain.create_user(users_model)
