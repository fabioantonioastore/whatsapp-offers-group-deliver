from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    def __init__(self, database_session: AsyncSession) -> None:
        self._database_session = database_session

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._database_session})"
