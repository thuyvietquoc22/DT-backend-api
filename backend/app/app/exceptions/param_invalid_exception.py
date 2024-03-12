from http import HTTPStatus

from app.exceptions.base_exception import BaseExceptionMixin


class ParamInvalidException(BaseExceptionMixin):

    def __init__(self, message: str = "Bad Request"):
        self.message = message
        self.status = HTTPStatus.BAD_REQUEST
