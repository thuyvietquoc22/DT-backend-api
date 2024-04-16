from fastapi import APIRouter, FastAPI

from app.core.config import settings
from app.routers.auth.admin_auth import AdminAuthRouter
from app.routers.cms import CMSRouterGroup
from app.routers.mobile.auth import MobileAuthRoute
from app.routers.cms.account import AccountRouter
from app.routers.cms.assets import AssetsRouter
from app.routers.cms.model import ModelRouter
from app.routers.cms.permission import PermissionRouter
from app.routers.cms.role import RoleRouter
from app.routers.desktop import DesktopRouter
from app.routers.mobile import MobileRouter
from app.routers.mobile.user import UserRouter


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
