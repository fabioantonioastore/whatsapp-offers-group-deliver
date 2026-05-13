from fastapi import HTTPException, status, Security
from fastapi.security import APIKeyHeader

from ..configs.environment import API_ACCESS_TOKEN

api_key_scheme = APIKeyHeader(name="X-API-Key")


async def verify_api_access_token(token: str = Security(api_key_scheme)) -> None:
    if token != API_ACCESS_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
