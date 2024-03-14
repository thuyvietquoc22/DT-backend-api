from typing import TypeVar, Generic

from pydantic.main import BaseModel

# D = List[somthing]
D = TypeVar('D', list, BaseModel)


class PaginationResponse(Generic[D], BaseModel):
    data: D
    pages: int
    items: int
    page: int
    limit: int

    @classmethod
    def response(cls, data: D, total_pages: int, total_items: int, page: int, limit: int):
        return cls(data=data, pages=total_pages, items=total_items, page=page, limit=limit)
