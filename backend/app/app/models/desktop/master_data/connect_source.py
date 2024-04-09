from typing import Optional

from pydantic import BaseModel


class ConnectSourceBase(BaseModel):
    name: str
    keyname: str


class ConnectSourceCreate(ConnectSourceBase):
    pass


class ConnectSourceUpdate(BaseModel):
    name: Optional[str] = None
    keyname: Optional[str] = None


class ConnectSourceResponse(ConnectSourceBase):
    pass
