from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from app.models.cms.model import Location
from app.sevices.map_4d.response.place_detail import AddressComponent


class GeoCodeItem(BaseModel):
    addressComponents: Optional[List[AddressComponent]] = None
    id: str
    name: str
    address: str
    location: Location
    types: List[str]


class GeoCodeResponse(BaseModel):
    result: List[GeoCodeItem]
    code: str
