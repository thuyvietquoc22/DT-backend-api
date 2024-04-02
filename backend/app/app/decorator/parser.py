from typing import TypeVar

from pydantic import TypeAdapter
from pymongo.cursor import Cursor

T = TypeVar('T')


def parse_as(response_type: type[T]) -> callable:
    """
    Nên dùng trong repository để parse data từ database thành kiểu dữ liệu mong muốn
    """

    def wrapper(func: callable):
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            if result is None:
                return None
            return TypeAdapter(response_type).validate_python(result)

        return inner

    return wrapper
