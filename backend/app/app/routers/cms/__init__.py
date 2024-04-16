from app.routers import BaseRouterGroup, BaseRouter
from app.routers.cms.account import AccountRouter
from app.routers.cms.assets import AssetsRouter
from app.routers.cms.model import ModelRouter
from app.routers.cms.permission import PermissionRouter
from app.routers.cms.role import RoleRouter


class CMSRouterGroup(BaseRouterGroup):
    @property
    def sub_routers(self) -> list[BaseRouter]:
        return [
            AccountRouter(),
            AssetsRouter(),
            ModelRouter(),
            PermissionRouter(),
            RoleRouter()
        ]
