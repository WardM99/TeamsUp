"""all crud opperation for a team"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Game, Team


async def create_team(database: AsyncSession, team_name: str, game: Game) -> Team:
    """Creates a new game"""
    team: Team = Team(team_name=team_name, game=game)
    database.add(team)
    await database.commit()
    return team


async def get_team(database: AsyncSession, team_id: int, game: Game) -> Team:
    """Returns a game"""
    query = select(Team).where(Team.team_id == team_id).where(Team.game == game)
    result = await database.execute(query)
    return result.unique().scalars().one()


async def get_all_teams_from_game(database: AsyncSession, game: Game) -> list[Team]:
    """returns all games"""
    query = select(Team).where(Team.game == game)
    result = await database.execute(query)
    return result.unique().scalars().all()


async def delete_team(database: AsyncSession, team: Team) -> None:
    """Deletes a team"""
    await database.delete(team)
    await database.commit()
