from typing import TypeVar, Callable

from pydantic import TypeAdapter
from pymongo.cursor import Cursor

T = TypeVar('T')


def parse_as(
        response_type: type[T],
        get_first: bool = False,
        exception_when_none=False,
        message_exception: str = None) -> Callable[[Callable[..., Cursor]], Callable[..., T]]:
    """
    Nên dùng trong repository để parse data từ database thành kiểu dữ liệu mong muốn
    """

    def wrapper(func: callable) -> Callable[..., response_type]:
        def inner(*args, **kwargs) -> response_type:
            result = func(*args, **kwargs)
            if result is None and not exception_when_none:
                return None
            elif result is None and exception_when_none:
                raise Exception(message_exception or "Không tìm thấy dữ liệu")

            if get_first:
                new_response_type = list[response_type]
                parsed = TypeAdapter(new_response_type).validate_python(result)
                if len(parsed) == 0 and exception_when_none:
                    raise Exception(message_exception or "Không tìm thấy dữ liệu")
                elif len(parsed) == 0 and not exception_when_none:
                    return None
                else:
                    return parsed[0]

            return TypeAdapter(response_type).validate_python(result)

        return inner

    return wrapper


def parse_val_as(
        value: any,
        response_type: type[T],
        get_first: bool = False,
        exception_when_none=False,
        message_exception: str = None) -> T:
    @parse_as(response_type, get_first, exception_when_none, message_exception)
    def returner():
        return value

    return returner()
