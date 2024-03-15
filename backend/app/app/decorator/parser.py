from typing import TypeVar

from pydantic import TypeAdapter
from pymongo.cursor import Cursor

T = TypeVar('T')


# Định nghĩa decorator parse_cursor_as
def parse_cursor_as(response_type: type[T]) -> callable:
    def wrapper(func: callable):
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, Cursor):
                return TypeAdapter(response_type).validate_python(result)
            return result

        return inner

    return wrapper
