from typing import Optional

from pydantic.main import BaseModel


class SubPermissionDomain(BaseModel):
    _str: str
    name: str


class PermissionDomain(BaseModel):
    id: str
    name: str
    sub_permissions: Optional[list[SubPermissionDomain]] = None
