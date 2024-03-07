from fastapi import APIRouter

from app.db.mongo_db import users_collection
from app.domain.auth.auth import AuthDomain, UserLoginModel


class AuthRouter:
    def __init__(self, auth_domain: AuthDomain) -> None:
        self.auth_domain = auth_domain

    @property
    def router(self):
        api_router = APIRouter(prefix='/auth', tags=['Auth'])

        @api_router.post('/register')
        async def login(user_login_model: UserLoginModel):
            new_user = await users_collection.insert_one(user_login_model.dict())

            return {
                'inserted_id': str(new_user.inserted_id),
            }

        return api_router
