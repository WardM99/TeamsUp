"""Logic of teams route"""
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.crud.team import get_all_teams_from_game, get_team, create_team
from src.database.models import Game, Team


async def logic_get_all_teams(database: AsyncSession, game: Game) -> list[Team]:
    """The logic to get all teams of a game"""
    return await get_all_teams_from_game(database, game)


async def logic_make_new_team(database: AsyncSession, game: Game, team_name: str) -> Team:
    """The logic to create a new team"""
    print(team_name)
    return await create_team(database, team_name, game)


async def logic_get_team_by_id(database: AsyncSession, game: Game,team_id: int) -> Team:
    """The logic to get a team by id"""
    return await get_team(database, team_id, game)
