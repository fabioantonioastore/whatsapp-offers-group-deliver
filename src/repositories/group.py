from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Group
from ..configs.environment import GROUP_TOTAL_PARTICIPANTS_SAFE_LIMIT


class GroupRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def get_first_not_full(self) -> Group | None:
        statement = select(Group).where(
            Group.total_participants < GROUP_TOTAL_PARTICIPANTS_SAFE_LIMIT
        )
        result = await self.__session.execute(statement=statement)
        return result.scalars().first()

    async def get_all(self) -> Sequence[Group]:
        statement = select(Group)
        result = await self.__session.execute(statement=statement)
        return result.scalars().all()

    async def get_by_jid(self, jid: str) -> Group:
        statement = select(Group).where(Group.jid == jid)
        result = await self.__session.execute(statement=statement)
        return result.scalars().one()

    async def create(self, group: Group) -> Group:
        self.__session.add(instance=group)
        return group

    async def delete(self, group: Group) -> None:
        await self.__session.delete(group)

    async def update_total_participants(
        self, group_jid: str, total_participants: int
    ) -> None:
        statement = (
            update(Group)
            .where(Group.jid == group_jid)
            .values(total_participants=total_participants)
        )
        await self.__session.execute(statement=statement)

    def __repr__(self) -> str:
        return f"GroupRepository({self.__session})"
