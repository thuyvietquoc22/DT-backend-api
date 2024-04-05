from fastapi import APIRouter

from app.domain.desktop.connection_source import ConnectSourceDomain, connection_source_domain
from app.routers import BaseRouter


class ConnectSourceRouter(BaseRouter):

    @property
    def connection_source_domain(self) -> ConnectSourceDomain:
        return connection_source_domain

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/connection-source", tags=["Desktop > Connection Source"])

        @router.get("")
        def get_connection_source():
            return self.connection_source_domain.get_connection_source()

        return router
