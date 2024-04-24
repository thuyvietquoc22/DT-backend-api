from typing import Literal

from app.models import BaseMongoModel


class VMSComponentCategoryResponse(BaseMongoModel):
    name: str
    type: Literal["IMAGE", "ARROW"]
    description: str
    keyname: str
