"""Teams routers"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.database import get_session
from src.app.logic.teams import (logic_get_all_teams,
                                 logic_make_new_team,
                                 logic_get_team_by_id,
                                 logic_join_team)
from src.app.logic.games import logic_get_game_by_id
from src.app.logic.players import require_player
from src.database.schemas.team import ReturnTeams, ReturnTeam, InputTeam
from src.database.models import Game, Player

teams_router = APIRouter(prefix="/teams")

@teams_router.get("", response_model=ReturnTeams, status_code=status.HTTP_200_OK,
                  dependencies=[Depends(require_player)])
async def get_teams(
    database: AsyncSession = Depends(get_session),
    game: Game = Depends(logic_get_game_by_id)
):
    """Get all teams of a game"""
    return ReturnTeams(teams=await logic_get_all_teams(database, game)) # type: ignore

@teams_router.post("", response_model=ReturnTeam, status_code=status.HTTP_201_CREATED,
                   dependencies=[Depends(require_player)])
async def make_team(
    input_team: InputTeam,
    database: AsyncSession = Depends(get_session),
    game: Game = Depends(logic_get_game_by_id)
):
    """Make new team for this game"""
    return await logic_make_new_team(database, game, input_team.team_name)


@teams_router.get("/{team_id}", response_model=ReturnTeam, status_code=status.HTTP_200_OK,
                  dependencies=[Depends(require_player)])
async def get_team_by_id(
    team_id: int, database: AsyncSession = Depends(get_session),
    game: Game = Depends(logic_get_game_by_id)
):
    """Get a team by id"""
    return await logic_get_team_by_id(database, game, team_id)


@teams_router.post("/{team_id}", response_model=ReturnTeam, status_code=status.HTTP_200_OK)
async def join_team(
    team_id: int, database: AsyncSession = Depends(get_session),
    game: Game = Depends(logic_get_game_by_id), player: Player = Depends(require_player)
):
    """Player joines a team"""
    return await logic_join_team(database, team_id, game, player)
