from http import HTTPStatus

from app.exceptions.base_exception import BaseExceptionMixin


class PageableException(BaseExceptionMixin):
    def __init__(self, message: str, page: int = 0, limit: int = 0):
        super().__init__(message=message)
        self.page = page
        self.limit = limit
        self.status = HTTPStatus.BAD_REQUEST
