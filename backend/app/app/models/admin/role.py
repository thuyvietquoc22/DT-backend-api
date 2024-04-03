from typing import Optional

from pydantic import BaseModel

from app.models import BaseMongoModel, PyObjectId
from app.models.admin.permission import PermissionResponse


class RoleBase(BaseMongoModel):
    name: str
    description: Optional[str] = None
    permission_ids: list[PyObjectId] = []


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleResponse(RoleBase):
    permissions: Optional[list[PermissionResponse]] = None
