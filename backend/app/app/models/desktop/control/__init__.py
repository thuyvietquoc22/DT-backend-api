from datetime import datetime
from typing import Literal, Optional

from app.models import BaseMongoModel, PyObjectId

ControlType = Literal['CAMERA', 'TRAFFIC_LIGHT', 'VMS_SIGN']


class BaseController(BaseMongoModel):
    """Các thuộc tính chung của một bộ điều khiển."""
    prev_control: Optional[PyObjectId]
    time_control: datetime
    device_id: PyObjectId
    control_type: ControlType
    # account_id: PyObjectId
