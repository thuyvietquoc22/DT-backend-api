from typing import TypeVar, Generic, Optional, List, Any

from pydantic.main import BaseModel

D = TypeVar('D', List, Any)


class Pageable(BaseModel):
    page: int
    limit: int
    pages: Optional[int] = None
    items: Optional[int] = None

    @property
    def skip(self):
        return (self.page - 1) * self.limit

    @classmethod
    def of(cls, page: int, limit: int):
        return cls(page=page, limit=limit, pages=None, items=None)


class PaginationResponse(Generic[D], BaseModel):
    data: D
    pages: int
    items: int
    page: int
    limit: int

    @classmethod
    def response(cls, data: D, total_pages: int, total_items: int, page: int, limit: int):
        return cls(data=data, pages=total_pages, items=total_items, page=page, limit=limit)

    @classmethod
    def response_pageable(cls, data: D, pageable: Pageable):
        return cls(data=data, pages=pageable.pages, items=pageable.items, page=pageable.page, limit=pageable.limit)
