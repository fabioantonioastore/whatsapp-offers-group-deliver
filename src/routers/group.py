from typing import Annotated, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, status, Depends, Request
from fastapi.responses import RedirectResponse, HTMLResponse

from ..dependencies.database import get_database_session
from ..dependencies.auth import verify_api_access_token
from ..manager import GroupManager
from ..schemas.group import CreateGroup, UpdateTotalParticipants, GroupResponse
from ..configs.rate_limit import limiter

router = APIRouter(prefix="/group")


@router.get(path="/redirect/invite_link", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")  # type: ignore
async def redirect_to_group_invite_link(
    request: Request,
    database_session: Annotated[AsyncSession, Depends(get_database_session)],
) -> HTMLResponse:
    group_manager = GroupManager(database_session=database_session)
    invite_link = await group_manager.get_available_group_invite_link()
    html_content = f"""
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Redirecionando...</title>
            <script>
                window.onload = function() {{
                    // Tenta abrir o link do WhatsApp por clique simulado ou atribuição
                    window.location.href = "{invite_link}";
                }};
            </script>
            <style>
                body {{ font-family: sans-serif; text-align: center; padding-top: 50px; }}
                .btn {{ padding: 10px 20px; background-color: #25D366; color: white; text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <p>Se você não for redirecionado automaticamente, clique abaixo:</p>
            <a class="btn" href="{invite_link}">Entrar no Grupo</a>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@router.post(path="", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")  # type: ignore
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
@limiter.limit("4/minute")  # type: ignore
async def get_all_groups(
    request: Request,
    _: Annotated[None, Depends(verify_api_access_token)],
    database_session: Annotated[AsyncSession, Depends(get_database_session)],
) -> Sequence[GroupResponse]:
    group_manager = GroupManager(database_session=database_session)
    return await group_manager.get_all()


@router.post(path="/fill_database", status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute") # type: ignore
async def fill_database(
    request: Request,
    _: Annotated[None, Depends(verify_api_access_token)],
    database_session: Annotated[AsyncSession, Depends(get_database_session)],
    data: list[CreateGroup]
) -> list[GroupResponse]:
    group_manager = GroupManager(database_session=database_session)
    return await group_manager.fill_database(data)
