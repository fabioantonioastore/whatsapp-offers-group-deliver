from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded

from .exceptions.rate_limit import rate_limit_exceeded_handler
from .routers import group_router
from .configs.environment import DEBUG


app = FastAPI(
    docs_url=None,
    redoc_url=None,
    debug=False
)
if DEBUG:
    app = FastAPI(
        debug=True
    )
app.add_exception_handler(
    exc_class_or_status_code=RateLimitExceeded, handler=rate_limit_exceeded_handler
)
app.include_router(group_router)
