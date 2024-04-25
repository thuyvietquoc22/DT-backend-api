from fastapi import APIRouter, FastAPI

from app.core.config import settings
from app.routers.cms import CMSRouterGroup
from app.routers.desktop import DesktopRouter
from app.routers.mobile import MobileRouter


def register_router(app: FastAPI):
    api_router = APIRouter()

    # Group routers
    desktop_router = DesktopRouter().router
    api_router.include_router(desktop_router)

    mobile_router = MobileRouter().router
    api_router.include_router(mobile_router)

    cms_router = CMSRouterGroup().router
    api_router.include_router(cms_router)

    app.include_router(api_router, prefix=settings.API_V1_STR)
