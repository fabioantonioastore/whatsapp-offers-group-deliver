from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from ..repositories import GroupRepository
from .base import BaseService
from ..models import Group
from ..schemas.group import CreateGroup, UpdateTotalParticipants


class GroupService(BaseService):
    def __init__(self, database_session: AsyncSession) -> None:
        super().__init__(database_session=database_session)
        self.__group_repository = GroupRepository(self._database_session)

    async def get_available_group_invite_link(self) -> str:
        try:
            group = await self.__group_repository.get_first_not_full()
            return group.invite_link
        except Exception as error:
            raise HTTPException(
                detail=f"Not found: {error}", status_code=status.HTTP_404_NOT_FOUND
            )

    async def create(self, group_data: CreateGroup) -> Group:
        group = Group(**group_data.model_dump())
        return await self.__group_repository.create(group=group)

    async def update_total_participants(self, data: UpdateTotalParticipants) -> None:
        await self.__group_repository.update_total_participants(
            group_jid=data.jid, total_participants=data.total_participants
        )

    async def get_all(self) -> Sequence[Group]:
        return await self.__group_repository.get_all()
