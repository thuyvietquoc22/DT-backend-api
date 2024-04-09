from typing import Optional

from pydantic import BaseModel


class ConnectSourceBase(BaseModel):
    name: str
    keyname: str


class ConnectSourceCreate(ConnectSourceBase):
    pass


class ConnectSourceUpdate(ConnectSourceBase):
    name: Optional[str]
    keyname: Optional[str]


class ConnectSourceResponse(ConnectSourceBase):
    pass
