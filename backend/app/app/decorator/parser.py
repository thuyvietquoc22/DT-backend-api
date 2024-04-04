from typing import TypeVar, Callable

from pydantic import TypeAdapter, BaseModel
from pymongo.cursor import Cursor

T = TypeVar('T')


def parse_as(response_type: type[T], get_first: bool = False) -> Callable[[Callable[..., Cursor]], Callable[..., T]]:
    """
    Nên dùng trong repository để parse data từ database thành kiểu dữ liệu mong muốn
    """

    def wrapper(func: callable) -> Callable[..., response_type]:
        def inner(*args, **kwargs) -> response_type:
            result = func(*args, **kwargs)
            if result is None:
                return None

            if get_first:
                new_response_type = list[response_type]
                parsed = TypeAdapter(new_response_type).validate_python(result)
                return parsed[0] if parsed and len(parsed) > 0 else None

            return TypeAdapter(response_type).validate_python(result)

        return inner

    return wrapper
