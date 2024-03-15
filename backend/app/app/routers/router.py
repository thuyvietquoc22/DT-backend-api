from fastapi import APIRouter, FastAPI

from app.core.config import settings
from app.domain.admin.permission import permission_domain
from app.domain.auth.admin_auth import admin_auth_domain
from app.domain.auth.mobile_auth import mobile_auth_domain
from app.domain.moblie.user import user_domain
from app.routers.admin.permission import PermissionRouter
from app.routers.auth.admin_auth import AdminAuthRouter
from app.routers.auth.mobile_auth import MobileAuthRoute
from app.routers.mobile.user import UserRouter


def register_router(app: FastAPI):
    api_router = APIRouter()

    mobile_auth_router = MobileAuthRoute(mobile_auth_domain).router
    api_router.include_router(mobile_auth_router)

    admin_auth_router = AdminAuthRouter(admin_auth_domain).router
    api_router.include_router(admin_auth_router)

    user_router = UserRouter(user_domain).router
    api_router.include_router(user_router)

    permission_router = PermissionRouter(permission_domain).router
    api_router.include_router(permission_router)

    app.include_router(api_router, prefix=settings.API_V1_STR)
