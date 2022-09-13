"""all crud opperation for a player"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Player

async def create_player(database: AsyncSession, team_id: int, name: str) -> Player:
    """Creates a new player"""
    player: Player = Player(
        team_id = team_id,
        name=name
    )
    database.add(player)
    await database.commit()
    return player


async def get_player(database: AsyncSession, player_id: int) -> Player:
    """Returns a player"""
    query = select(Player).where(Player.player_id == player_id)
    result = await database.execute(query)
    return result.unique().scalars().all()


async def delete_player(database: AsyncSession, player: Player) -> None:
    """Deletes a player"""
    await database.delete(player)
    await database.commit()
