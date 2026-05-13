from typing import Annotated, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, status, Depends, Request

from ..dependencies.database import get_database_session
from ..dependencies.auth import verify_api_access_token
from ..manager import GroupManager
from ..schemas.group import CreateGroup, UpdateTotalParticipants, GroupResponse
from ..configs.rate_limit import limiter

router = APIRouter(prefix="/group")


@router.get(
    path="/invite_link",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": "https://chat.whatsapp.com/asetdEdkl3190DSFnDSdjq"
                }
            }
        }
    },
)
@limiter.limit("1000/minute")  # type: ignore
async def get_available_group_invite_link(
    request: Request,
    database_session: Annotated[AsyncSession, Depends(get_database_session)],
) -> str:
    group_manager = GroupManager(database_session=database_session)
    return await group_manager.get_available_group_invite_link()


@router.post(path="", status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")  # type: ignore
async def create_group(
    request: Request,
    data: CreateGroup,
    _: Annotated[None, Depends(verify_api_access_token)],
    database_session: Annotated[AsyncSession, Depends(get_database_session)],
) -> GroupResponse:
    group_manager = GroupManager(database_session=database_session)
    return await group_manager.create(group_data=data)


@router.patch(path="/total_participants", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("1000/minute")  # type: ignore
async def patch_total_participants(
    request: Request,
    data: UpdateTotalParticipants,
    _: Annotated[None, Depends(verify_api_access_token)],
    database_session: Annotated[AsyncSession, Depends(get_database_session)],
) -> None:
    group_manager = GroupManager(database_session=database_session)
    await group_manager.update_total_participants(data=data)


@router.get(path="/all", status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")  # type: ignore
async def get_all_groups(
    request: Request,
    _: Annotated[None, Depends(verify_api_access_token)],
    database_session: Annotated[AsyncSession, Depends(get_database_session)],
) -> Sequence[GroupResponse]:
    group_manager = GroupManager(database_session=database_session)
    return await group_manager.get_all()
