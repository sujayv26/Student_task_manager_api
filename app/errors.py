from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def error_body(message: str):
    return {
        "success": False,
        "message": message,
        "data": None,
    }


def error_response(status_code: int, message: str):
    return JSONResponse(
        status_code=status_code,
        content=error_body(message),
    )


def task_not_found(_task_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found",
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(_request: Request, exc: StarletteHTTPException):
        if exc.status_code == status.HTTP_404_NOT_FOUND:
            message = "Task not found"
        elif isinstance(exc.detail, str):
            message = exc.detail
        else:
            message = "Request failed"
        return error_response(exc.status_code, message)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_request: Request, _exc: RequestValidationError):
        return error_response(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Validation error",
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_request: Request, _exc: Exception):
        return error_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred. Please try again later.",
        )
