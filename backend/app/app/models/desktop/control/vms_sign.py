from typing import Literal

from pydantic import BaseModel

from app.models import PyObjectId
from app.models.desktop.control import BaseController, ControlType


class SimpleVMSSignItem(BaseModel):
    width: float
    height: float
    top: float
    left: float


class TextComponent(SimpleVMSSignItem):
    content: str
    text_align: Literal["left", "center", "right"]
    font_size: float


class ImageComponent(SimpleVMSSignItem):
    vms_component_id: PyObjectId


class BaseVMSSignController(BaseModel):
    texts: list[TextComponent]
    images: list[ImageComponent]


class VMSSignController(BaseVMSSignController, BaseController):
    control_type: ControlType = "VMS_SIGN"
    pass


class VMSSignRequest(BaseVMSSignController):
    pass
