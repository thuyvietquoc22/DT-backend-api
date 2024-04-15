from typing import List

from app.models.cms.model import Location
from app.sevices.map_4d.response import BaseMap4DServiceResult


class TextSearchResponse(BaseMap4DServiceResult):
    id: str
    name: str
    address: str
    location: Location
    types: List[str]
