from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseManager
from ..services import GroupService
from ..schemas.group import CreateGroup, UpdateTotalParticipants, GroupResponse


class GroupManager(BaseManager):
    def __init__(self, database_session: AsyncSession) -> None:
        super().__init__()
        self.__database_session = database_session
        self.__group_service = GroupService(self.__database_session)

    async def get_available_group_invite_link(self) -> str:
        return await self.__group_service.get_available_group_invite_link()

    async def create(self, group_data: CreateGroup) -> GroupResponse:
        group = await self.__group_service.create(group_data=group_data)
        return GroupResponse(
            jid=group.jid,
            invite_link=group.invite_link,
            total_participants=group.total_participants,
        )

    async def fill_database(self, groups_data: list[CreateGroup]) -> list[GroupResponse]:
        response: list[GroupResponse] = []
        for group in groups_data:
            response.append(await self.create(group_data=group))
        return response

    async def update_total_participants(self, data: UpdateTotalParticipants) -> None:
        await self.__group_service.update_total_participants(data=data)

    async def get_all(self) -> Sequence[GroupResponse]:
        groups = await self.__group_service.get_all()
        return [
            GroupResponse(
                jid=group.jid,
                invite_link=group.invite_link,
                total_participants=group.total_participants,
            )
            for group in groups
        ]
