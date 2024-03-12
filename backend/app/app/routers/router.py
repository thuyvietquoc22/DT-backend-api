from fastapi import APIRouter, FastAPI

from app.core.config import settings
from app.routers.auth.auth import AuthRouter


def register_router(app: FastAPI):
    api_router = APIRouter()

    auth_router = AuthRouter()
    api_router.include_router(auth_router.router)

    app.include_router(api_router, prefix=settings.API_V1_STR)
