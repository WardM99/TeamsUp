"""Players routers"""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.database import get_session
from src.app.logic.players import ( logic_make_new_player,
                                    logic_generate_token,
                                    require_player,
                                    logic_get_player_by_name_and_password)
from src.database.models import Player
from src.database.schemas.player import Token, InputPlayer, ReturnPlayer

players_router = APIRouter(prefix=("/players"))

@players_router.post("", response_model=Token, status_code=status.HTTP_201_CREATED)
async def new_player(input_player: InputPlayer, database: AsyncSession = Depends(get_session)):
    """Make a new player"""
    player: Player = await logic_make_new_player(database, input_player.name, input_player.password)
    return await logic_generate_token(player)


@players_router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                datatbase: AsyncSession= Depends(get_session)):
    """Login a player"""
    player: Player = await logic_get_player_by_name_and_password(datatbase,
                                                                 form_data.username,
                                                                 form_data.password)
    return await logic_generate_token(player)


@players_router.get("/current", response_model=ReturnPlayer, status_code=status.HTTP_200_OK)
async def current_player(player: Player = Depends(require_player)):
    """route to get the loged in player"""
    return player
