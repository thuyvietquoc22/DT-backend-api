from fastapi import APIRouter, FastAPI

from app.core.config import settings
from app.domain.auth.admin_auth import admin_auth_domain
from app.domain.auth.mobile_auth import mobile_auth_domain
from app.domain.cms.assets import assets_domain
from app.domain.cms.model import model_domain
from app.domain.cms.permission import permission_domain
from app.domain.cms.role import role_domain
from app.domain.moblie.user import user_domain
from app.routers.auth.admin_auth import AdminAuthRouter
from app.routers.auth.mobile_auth import MobileAuthRoute
from app.routers.cms.account import AccountRouter
from app.routers.cms.assets import AssetsRouter
from app.routers.cms.model import ModelRouter
from app.routers.cms.permission import PermissionRouter
from app.routers.cms.role import RoleRouter
from app.routers.desktop import DesktopRouter
from app.routers.desktop.address import DesktopAddressRouter
from app.routers.mobile.user import UserRouter


def register_router(app: FastAPI):
    api_router = APIRouter()

    desktop_router = DesktopRouter().router
    api_router.include_router(desktop_router)

    mobile_auth_router = MobileAuthRoute(mobile_auth_domain).router
    api_router.include_router(mobile_auth_router)

    admin_auth_router = AdminAuthRouter(admin_auth_domain).router
    api_router.include_router(admin_auth_router)

    user_router = UserRouter(user_domain).router
    api_router.include_router(user_router)

    permission_router = PermissionRouter(permission_domain).router
    api_router.include_router(permission_router)

    role_router = RoleRouter(role_domain).router
    api_router.include_router(role_router)

    assets_router = AssetsRouter(assets_domain).router
    api_router.include_router(assets_router)

    model_router = ModelRouter(model_domain).router
    api_router.include_router(model_router)

    account_router = AccountRouter().router
    api_router.include_router(account_router)

    app.include_router(api_router, prefix=settings.API_V1_STR)
