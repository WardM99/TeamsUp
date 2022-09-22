"""Players routers"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.database import get_session
from src.app.logic.players import (logic_get_all_players,
                                   logic_make_new_player,
                                   logic_get_player_by_id,
                                   logic_generate_token)
from src.app.logic.teams import logic_get_team_by_id
from src.database.schemas.player import ReturnPlayer, ReturnPlayers, InputPlayer, Token
from src.database.models import Team

players_router = APIRouter(prefix="/players")

@players_router.get("", response_model=ReturnPlayers, status_code=status.HTTP_200_OK)
async def get_players(
    database: AsyncSession = Depends(get_session),
    team: Team = Depends(logic_get_team_by_id)
):
    """Get all players of a team"""
    return ReturnPlayers(players=await logic_get_all_players(database, team))


@players_router.post("", response_model=Token, status_code=status.HTTP_201_CREATED)
async def make_player(
    input_player: InputPlayer,
    database: AsyncSession = Depends(get_session),
    team: Team = Depends(logic_get_team_by_id)
):
    """Make a new player for this team"""
    return await logic_generate_token(
        await logic_make_new_player(database, team, input_player.name)
    )
    #return await logic_make_new_player(database, team, input_player.name)


@players_router.get("/{player_id}", response_model=ReturnPlayer, status_code=status.HTTP_200_OK)
async def get_player_by_id(
    player_id: int,
    database: AsyncSession = Depends(get_session),
    team: Team = Depends(logic_get_team_by_id)
):
    """Get a player by id"""
    return await logic_get_player_by_id(database, team, player_id)
    