from fastapi import Request, FastAPI
from starlette.responses import JSONResponse

from app.exceptions.base_exception import BaseExceptionMixin


def __handle_exception(request: Request, ex: BaseExceptionMixin):
    return JSONResponse(
        status_code=ex.status.value,
        content=dict(status=ex.status, message=ex.message, path=request.url.path)
    )


def register_exception_handler(app: FastAPI):
    @app.exception_handler(BaseExceptionMixin)
    def base_exception_handler(request: Request, ex: BaseExceptionMixin):
        return __handle_exception(request, ex)

    @app.exception_handler(Exception)
    def exception_handler(request: Request, ex: Exception):
        return __handle_exception(request, BaseExceptionMixin(message=str(ex)))
