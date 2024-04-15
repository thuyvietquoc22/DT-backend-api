from fastapi import APIRouter, FastAPI

from app.core.config import settings
from app.sevices.auth.admin_auth import admin_auth_service
from app.sevices.auth.mobile_auth import mobile_auth_service
from app.sevices.cms.assets import assets_service
from app.sevices.cms.model import model_service
from app.sevices.cms.permission import permission_service
from app.sevices.cms.role import role_service
from app.sevices.moblie.user import user_service
from app.routers.auth.admin_auth import AdminAuthRouter
from app.routers.auth.mobile_auth import MobileAuthRoute
from app.routers.cms.account import AccountRouter
from app.routers.cms.assets import AssetsRouter
from app.routers.cms.model import ModelRouter
from app.routers.cms.permission import PermissionRouter
from app.routers.cms.role import RoleRouter
from app.routers.desktop import DesktopRouter
from app.routers.mobile.user import UserRouter


def register_router(app: FastAPI):
    api_router = APIRouter()

    desktop_router = DesktopRouter().router
    api_router.include_router(desktop_router)

    mobile_auth_router = MobileAuthRoute().router
    api_router.include_router(mobile_auth_router)

    admin_auth_router = AdminAuthRouter(admin_auth_service).router
    api_router.include_router(admin_auth_router)

    user_router = UserRouter(user_service).router
    api_router.include_router(user_router)

    permission_router = PermissionRouter().router
    api_router.include_router(permission_router)

    role_router = RoleRouter().router
    api_router.include_router(role_router)

    assets_router = AssetsRouter().router
    api_router.include_router(assets_router)

    model_router = ModelRouter().router
    api_router.include_router(model_router)

    account_router = AccountRouter().router
    api_router.include_router(account_router)

    app.include_router(api_router, prefix=settings.API_V1_STR)
