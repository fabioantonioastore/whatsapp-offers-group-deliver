from sqlalchemy.ext.asyncio import async_sessionmaker

from .engine import async_engine

async_session_factory = async_sessionmaker(async_engine)
