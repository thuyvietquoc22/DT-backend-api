from typing import Literal, Optional

from pydantic import BaseModel, field_serializer

from app.models import BaseMongoModel
from app.models.desktop.master_data.vms_component_category import VMSComponentCategoryResponse
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
    category_key: str


class VMSComponentUpdate(BaseModel):
    type: Optional[Literal["IMAGE", "ARROW"]] = None
    name: Optional[str] = None
    code: Optional[int] = None
    meaning: Optional[str] = None
    category_key: Optional[str] = None


class VMSComponentResponse(BaseVMSComponent):
    category: VMSComponentCategoryResponse

    @field_serializer("category")
    def serialize_category(self, category: VMSComponentCategoryResponse):
        return category.model_dump(exclude={"type", "description"})
