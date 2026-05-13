from sqlalchemy.ext.asyncio import create_async_engine

from ...configs.environment import DATABASE_URL

async_engine = create_async_engine(url=DATABASE_URL)
