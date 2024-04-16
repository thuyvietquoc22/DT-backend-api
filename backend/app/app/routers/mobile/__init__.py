from fastapi import APIRouter

from app.routers import BaseRouter, BaseRouterGroup
from app.routers.mobile.auth import MobileAuthRoute
from app.routers.mobile.user import UserRouter


class MobileRouter(BaseRouterGroup):

    @property
    def prefix(self) -> str:
        return '/mobile'

    @property
    def sub_routers(self) -> list[BaseRouter]:
        return [
            UserRouter(),
            MobileAuthRoute()
        ]
