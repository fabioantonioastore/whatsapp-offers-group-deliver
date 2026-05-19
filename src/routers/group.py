from typing import Annotated, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, status, Depends, Request
from fastapi.responses import HTMLResponse

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
    app_invite_link = invite_link.replace("https", "whatsapp")
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Redirecionando para o Grupo...</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
                background-color: #f0f2f5;
            }}
            .btn {{
                background-color: #25D366;
                color: white;
                padding: 15px 30px;
                border-none;
                border-radius: 25px;
                text-decoration: none;
                font-weight: bold;
                font-size: 18px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
        </style>
    </head>
    <body>
        <h2>Abrindo o WhatsApp...</h2>
        <p>Se o aplicativo não abrir automaticamente, clique no botão abaixo:</p>
        <a href="{invite_link}" id="zap-link" class="btn">Entrar no Grupo</a>

        <script>
            // Tenta abrir direto no aplicativo usando o protocolo nativo
            window.location.href = "{app_invite_link}";
            
            // Se o usuário continuar na página após 1.5 segundos, 
            // altera o link principal para a versão web padrão por segurança
            setTimeout(function() {{
                window.location.href = "{invite_link}";
            }}, 1500);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


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
