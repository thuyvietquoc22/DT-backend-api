from __future__ import annotations

from typing import Any, List, Optional, Literal

import numpy
from pydantic import BaseModel

from app.models.cms.model import Location


class TypeInfo(BaseModel):
    id: str
    name: str
    group: str


class MainTypeInfos(BaseModel):
    id: str
    name: str
    group: str


class AddressComponent(BaseModel):
    types: List[str]
    name: str


class CreatedBy(BaseModel):
    userId: str
    displayName: str


class UpdatedBy(BaseModel):
    userId: str
    displayName: str


class PlaceType(BaseModel):
    id: str
    name: str
    description: str
    minZoom: Any
    group: str
    minRank: Any
    maxRank: Any
    icon: Any
    createdBy: CreatedBy
    updatedBy: UpdatedBy
    createdDate: int
    updatedDate: int


class Geometry(BaseModel):
    type: str
    coordinates: List[Any]


class Rank(BaseModel):
    value: int


class ReviewsSummary(BaseModel):
    ratingAverage: int
    totalRating: int
    numberOfRatingOneStar: int
    numberOfRatingTwoStar: int
    numberOfRatingThreeStar: int
    numberOfRatingFourStar: int
    numberOfRatingFiveStar: int


class PlaceDetailResult(BaseModel):
    id: str
    location: Location
    address: str
    name: str
    objectId: Any
    description: Optional[str]
    types: List[str]
    mainType: str
    addressComponents: List[AddressComponent]
    tags: List[str]
    geometry: Geometry
    isDeleted: bool

    @property
    def flat_coordinates(self):
        result = []
        for i in self.geometry.coordinates:
            result += i
        return result


class PlaceDetailResponse(BaseModel):
    code: Literal["id_not_found", "ok"]
    result: PlaceDetailResult
