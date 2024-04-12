from typing import List
from pydantic import BaseModel

from app.models.cms.model import Location
from app.utils.map_4d_service.response import BaseMap4DServiceResult


class TextSearchResponse(BaseMap4DServiceResult):
    id: str
    name: str
    address: str
    location: Location
    types: List[str]
