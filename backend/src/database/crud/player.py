"""all crud opperation for a player"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Player

async def create_player(database: AsyncSession, name: str, password: str) -> Player:
    """Creates a new player"""
    print(password)
    player: Player = Player(
        name=name,
        password=password
    )
    database.add(player)
    await database.commit()
    return player


async def delete_player(database: AsyncSession, player: Player) -> None:
    """Deletes a player"""
    await database.delete(player)
    await database.commit()


async def get_player_by_id(database: AsyncSession, player_id: int) -> Player:
    """Return a player by id"""
    query = select(Player).where(Player.player_id == player_id)
    result = await database.execute(query)
    return result.unique().scalars().one()


async def get_player_by_name(database: AsyncSession,
                             name: str) -> Player:
    """Return a player by login"""
    query = select(Player).where(Player.name == name)
    result = await database.execute(query)
    return result.unique().scalars().one()
