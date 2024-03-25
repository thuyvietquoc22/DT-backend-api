from http import HTTPStatus

from app.exceptions.base_exception import BaseExceptionMixin


class NotFoundException(BaseExceptionMixin):
    status = HTTPStatus.NOT_FOUND

    def __init__(self, message: str = "Not Found"):
        self.message = message
        self.status = HTTPStatus.NOT_FOUND
