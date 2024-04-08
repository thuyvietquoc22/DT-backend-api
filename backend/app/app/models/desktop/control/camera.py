from typing import Optional

from pydantic import BaseModel

from app.models.desktop.control import BaseController


class CameraControl(BaseController):
    angle_x: float
    angle_y: float
    zoom: float
    focus: float
    iris: float


class CameraControlRequest(BaseModel):
    camera_id: str = None
    angle_x: Optional[float] = None
    angle_y: Optional[float] = None
    zoom: Optional[float] = None
    focus: Optional[float] = None
    iris: Optional[float] = None
