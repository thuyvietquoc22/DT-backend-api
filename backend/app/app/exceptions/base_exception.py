# exception
from http import HTTPStatus
from locale import str


class BaseExceptionMixin(Exception):
    status: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR
    message: str

    def __init__(self, message: str = None, status: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR):
        self.message = message or self.message or "Unknown Error"
        self.status = status or self.status
