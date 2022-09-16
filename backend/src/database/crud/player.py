"""all crud opperation for a player"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Player, Game, Team

async def create_player(database: AsyncSession, team_id: int, name: str) -> Player:
    """Creates a new player"""
    player: Player = Player(
        team_id = team_id,
        name=name
    )
    database.add(player)
    await database.commit()
    return player


async def get_player(database: AsyncSession, player_id: int, team: Team) -> Player:
    """Returns a player"""
    query = select(Player).where(Player.team == team).where(Player.player_id == player_id)
    result = await database.execute(query)
    return result.unique().scalars().one()


async def get_players_game(database: AsyncSession, game: Game) -> list[Player]:
    """Returns all players of a game"""
    subquery = select(Team.team_id).where(Team.game == game)
    query = select(Player).filter(Player.team_id.in_(subquery))
    result = await database.execute(query)
    return result.unique().scalars().all()


async def get_players_team(database: AsyncSession, team: Team) -> list[Player]:
    """Returns all palyers of a team"""
    query = select(Player).where(Player.team == team)
    result = await database.execute(query)
    return result.unique().scalars().all()


async def delete_player(database: AsyncSession, player: Player) -> None:
    """Deletes a player"""
    await database.delete(player)
    await database.commit()
