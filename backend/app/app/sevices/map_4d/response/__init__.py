from typing import TypeVar, Generic, Optional

from pydantic import BaseModel, Field


class BaseMap4DServiceResult(BaseModel):
    pass


# D class Các class kế thừ từ BaseMap4DServiceResult
D = TypeVar('D', bound=BaseMap4DServiceResult)


class Map4DServiceResponse(BaseModel, Generic[D]):
    code: str
    message: Optional[str] = None
    results: list[D] = Field(default=[], alias='result')
