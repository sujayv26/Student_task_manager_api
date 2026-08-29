from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

ERROR_NAMES = {
    400: "bad_request",
    404: "not_found",
    405: "method_not_allowed",
    422: "validation_error",
    500: "internal_server_error",
}


def error_body(status_code: int, message: str, details=None, error: str | None = None):
    body = {
        "error": error or ERROR_NAMES.get(status_code, "error"),
        "message": message,
        "status_code": status_code,
    }
    if details is not None:
        body["details"] = details
    return body


def error_response(status_code: int, message: str, details=None, error: str | None = None):
    return JSONResponse(
        status_code=status_code,
        content=error_body(status_code, message, details=details, error=error),
    )


def task_not_found(task_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with id {task_id} not found",
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(_request: Request, exc: StarletteHTTPException):
        message = exc.detail if isinstance(exc.detail, str) else "Request failed"
        return error_response(exc.status_code, message)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_request: Request, exc: RequestValidationError):
        details = []
        for err in exc.errors():
            loc = [part for part in err.get("loc", ()) if part != "body"]
            details.append(
                {
                    "field": ".".join(str(part) for part in loc) or "body",
                    "message": err.get("msg", "Invalid value"),
                }
            )
        return error_response(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Invalid request data",
            details=details,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_request: Request, _exc: Exception):
        return error_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred. Please try again later.",
        )
