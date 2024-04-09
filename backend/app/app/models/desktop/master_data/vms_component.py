from typing import Literal, Optional

from pydantic import BaseModel

from app.models import BaseMongoModel
from app.utils.cloudinary import CloudinaryEnabler


class BaseVMSComponent(BaseMongoModel, CloudinaryEnabler):
    type: Literal["IMAGE", "ARROW"]
    name: str
    code: int
    meaning: str
    url: str

    @property
    def folder(self):
        return f"VMS_COMPONENT/{self.type}"

    @property
    def public_id(self):
        if self.url in [None, ""]:
            return None
        index = self.url.rfind("VMS_COMPONENT")
        return self.url[index:].split(".")[0]


class VMSComponentCreate(BaseVMSComponent):
    pass


class VMSComponentUpdate(BaseModel):
    type: Optional[Literal["IMAGE", "ARROW"]] = None
    name: Optional[str] = None
    code: Optional[int] = None
    meaning: Optional[str] = None


class VMSComponentResponse(BaseVMSComponent):
    pass
