"""Logic of teams route"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.logic.games import logic_get_game_by_id
from src.database.crud.team import get_all_teams_from_game, get_team, create_team, add_player
from src.database.database import get_session
from src.database.models import Game, Team, Player


async def logic_get_all_teams(database: AsyncSession, game: Game) -> list[Team]:
    """The logic to get all teams of a game"""
    return await get_all_teams_from_game(database, game)


async def logic_make_new_team(database: AsyncSession, game: Game, team_name: str) -> Team:
    """The logic to create a new team"""
    print(team_name)
    return await create_team(database, team_name, game)


async def logic_get_team_by_id(
    database: AsyncSession = Depends(get_session),
    game: Game = Depends(logic_get_game_by_id),
    team_id: int = 0
) -> Team:
    """The logic to get a team by id"""
    return await get_team(database, team_id, game)


async def logic_join_team(database: AsyncSession, team_id: int, game: Game, player: Player) -> Team:
    """The logic to join a team"""
    team: Team = await get_team(database, team_id, game)
    await add_player(database, team, player)
    return team
