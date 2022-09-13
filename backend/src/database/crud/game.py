"""all crud opperation for a game"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Game


async def create_game(database: AsyncSession) -> Game:
    """Creates a new game"""
    game: Game = Game()
    database.add(game)
    await database.commit()
    return game


async def get_game(database: AsyncSession, game_id: int) -> Game:
    """Returns a game"""
    query = select(Game).where(Game.game_id == game_id)
    result = await database.execute(query)
    return result.unique().scalars().all()
