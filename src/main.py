from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded

from .exceptions.rate_limit import rate_limit_exceeded_handler
from .routers import group_router

app = FastAPI(
    # docs_url=None,
    # redoc_url=None
)
app.add_exception_handler(
    exc_class_or_status_code=RateLimitExceeded, handler=rate_limit_exceeded_handler
)
app.include_router(group_router)
