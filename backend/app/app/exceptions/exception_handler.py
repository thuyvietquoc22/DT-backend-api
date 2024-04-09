from http import HTTPStatus
from typing import Type, Optional

from bson.errors import InvalidId
from fastapi import Request, FastAPI
from fastapi.exceptions import ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.responses import JSONResponse

from app.exceptions.base_exception import BaseExceptionMixin


def __get_app_middleware(app: FastAPI, middleware_class: Type) -> Optional[Middleware]:
    middleware_index = None

    for index, middleware in enumerate(app.user_middleware):
        if middleware.cls == middleware_class:
            middleware_index = index
    return None if middleware_index is None else app.user_middleware[middleware_index]


def __check_cors(request: Request, response: JSONResponse):
    cors_middleware = __get_app_middleware(app=request.app, middleware_class=CORSMiddleware)
    request_origin = request.headers.get("origin", "")
    if cors_middleware and "*" in cors_middleware.kwargs["allow_origins"]:
        response.headers["Access-Control-Allow-Origin"] = "*"
    elif cors_middleware and request_origin in cors_middleware.kwargs["allow_origins"]:
        response.headers["Access-Control-Allow-Origin"] = request_origin

    return response


def __handle_exception(request: Request, ex: BaseExceptionMixin):
    response = JSONResponse(
        status_code=ex.status.value,
        content=dict(status=ex.status, message=ex.message, path=request.url.path)
    )
    return __check_cors(request, response)


def register_exception_handler(app: FastAPI):
    @app.exception_handler(BaseExceptionMixin)
    def base_exception_handler(request: Request, ex: BaseExceptionMixin):
        return __handle_exception(request, ex)

    @app.exception_handler(Exception)
    def exception_handler(request: Request, ex: Exception):
        return __handle_exception(request, BaseExceptionMixin(message=str(ex)))

    @app.exception_handler(InvalidId)
    def invalid_id_exception_handler(request: Request, ex: InvalidId):
        message = str(ex)
        part = message.split("'")
        if len(part) == 3 and "is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string" in \
                part[2]:
            message = f"Id \"{part[1]}\" không hợp lệ"

        return __handle_exception(request, BaseExceptionMixin(message=message, status=HTTPStatus.BAD_REQUEST))

    @app.exception_handler(ResponseValidationError)
    def response_validation_error_handler(request: Request, ex: ResponseValidationError):
        if ex.body is None:
            return __handle_exception(request, BaseExceptionMixin(message=str("Not found data"),
                                                                  status=HTTPStatus.NOT_FOUND))
        raise ex
