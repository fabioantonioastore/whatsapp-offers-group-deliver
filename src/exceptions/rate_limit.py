from fastapi import Request, Response, status
from fastapi.responses import JSONResponse


def rate_limit_exceeded_handler(request: Request, exc: Exception) -> Response:
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Too many requests, try again later"},
    )
