from typing import Optional

from pydantic import Field

from app.models import BaseMongoModel


class BaseBusConnection(BaseMongoModel):
    code: str = ""
    provider: str = ""
    connection_source: str
    ip_address: str = Field(pattern=r'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b')
    username: str
    password: str


# class BusConnectionPayload(BaseBusConnection):
# bus_router_id: Optional[str] = None


class BusConnectionCreate(BaseBusConnection):
    bus_router_id: str


class BusConnectionUpdate(BaseMongoModel):
    code: Optional[str] = None
    provider: Optional[str] = None
    connection_source: Optional[str] = None
    ip_address: Optional[str] = Field(default=None, pattern=r'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b')
    username: Optional[str] = None
    password: Optional[str] = None
    bus_router_id: Optional[str] = None


class BusConnectionResponse(BaseBusConnection):
    pass

