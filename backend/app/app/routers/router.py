from fastapi import APIRouter, FastAPI

from app.core.config import settings
from app.routers.admin.permission import role_router
from app.routers.auth.auth import auth_router
from app.routers.mobile.mobile_auth import mobile_auth_router
from app.routers.mobile.user import user_router


def register_router(app: FastAPI):
    api_router = APIRouter()

    api_router.include_router(auth_router.router)
    api_router.include_router(mobile_auth_router.router)
    api_router.include_router(user_router.router)
    api_router.include_router(role_router.router)

    app.include_router(api_router, prefix=settings.API_V1_STR)
