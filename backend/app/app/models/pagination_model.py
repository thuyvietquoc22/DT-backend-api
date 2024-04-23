from typing import TypeVar, Generic, Optional, List, Any

from pydantic import Field, validator, field_validator
from pydantic.main import BaseModel

from app.exceptions.pageable_exception import PageableException

D = TypeVar('D', List, Any)


class Pageable(BaseModel):
    page: int
    limit: int
    pages: Optional[int] = None
    items: Optional[int] = None

    @property
    def skip(self):
        return (self.page - 1) * self.limit

    @property
    def pipeline(self):
        return [
            {"$skip": self.skip},
            {"$limit": self.limit}
        ]

    @classmethod
    def of(cls, page: int, limit: int):
        return cls(page=page, limit=limit, pages=None, items=None)

    @field_validator("page")
    def validate_page(cls, value):
        if value < 1:
            raise PageableException("Page must be greater than 0")
        return value

    @field_validator("limit")
    def validate_limit(cls, value):
        if value < 1:
            raise PageableException("Limit must be greater than 0")
        return value


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
