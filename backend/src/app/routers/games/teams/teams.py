"""Teams routers"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.database import get_session
from src.app.logic.teams import logic_get_all_teams, logic_make_new_team, logic_get_team_by_id
from src.app.logic.games import logic_get_game_by_id
from src.database.schemas.team import ReturnTeams, ReturnTeam, InputTeam
from src.database.models import Game
from src.app.routers.games.teams.players.players import players_router

teams_router = APIRouter(prefix="/teams")

teams_router.include_router(players_router, prefix="/{team_id}")

@teams_router.get("", response_model=ReturnTeams, status_code=status.HTTP_200_OK)
async def get_teams(
    database: AsyncSession = Depends(get_session),
    game: Game = Depends(logic_get_game_by_id)
):
    """Get all teams of a game"""
    return ReturnTeams(teams=await logic_get_all_teams(database, game))

@teams_router.post("", response_model=ReturnTeam, status_code=status.HTTP_201_CREATED)
async def make_team(
    input_team: InputTeam,
    database: AsyncSession = Depends(get_session),
    game: Game = Depends(logic_get_game_by_id)
):
    """Make new team for this game"""
    return await logic_make_new_team(database, game, input_team.team_name)


@teams_router.get("/{team_id}", response_model=ReturnTeam, status_code=status.HTTP_200_OK)
async def get_team_by_id(
    team_id: int, database: AsyncSession = Depends(get_session),
    game: Game = Depends(logic_get_game_by_id)
):
    """Get a team by id"""
    return await logic_get_team_by_id(database, game, team_id)
