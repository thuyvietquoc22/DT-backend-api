from abc import ABC, abstractmethod

from fastapi import APIRouter

from app.decorator import signleton


class BaseRouter(ABC):
    @property
    @abstractmethod
    def router(self) -> APIRouter:
        pass


class BaseRouterGroup(BaseRouter):
    @property
    @abstractmethod
    def sub_routers(self) -> list[BaseRouter]:
        pass

    @property
    def prefix(self) -> str:
        return ""

    @property
    def tags(self) -> list[str]:
        return []

    @property
    def router(self) -> APIRouter:
        api_router = APIRouter(prefix=self.prefix, tags=self.tags)
        for router in self.sub_routers:
            api_router.include_router(router.router)
        return api_router


class BaseTag:
    @property
    def root(self):
        return ""

    def get(self, name: str, is_mater_data: bool = False):
        result = []
        if is_mater_data:
            result.append(f"{self.root} - Master Data > {name}")
            # result.append(f"Master Data > {self.root}")
        else:
            result.append(f"{self.root} > {name}")
        return result


@signleton.singleton
class DesktopTag(BaseTag):
    root: str = "Desktop"


@signleton.singleton
class CMSTag(BaseTag):
    root: str = "CMS"


@signleton.singleton
class MobileTag(BaseTag):
    root: str = "Mobile"
