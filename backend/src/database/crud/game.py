"""all crud opperation for a game"""
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Game, Player


async def create_game(database: AsyncSession, owner: Player) -> Game:
    """Creates a new game"""
    game: Game = Game(owner=owner, cards=[])
    database.add(game)
    await database.commit()
    return game


async def get_game(database: AsyncSession, game_id: int) -> Game:
    """Returns a game"""
    query = select(Game).where(Game.game_id == game_id).options(selectinload(Game.cards)).options(selectinload(Game.teams))
    result = await database.execute(query)
    return result.unique().scalars().one()


async def get_all_games(database: AsyncSession) -> list[Game]:
    """returns all games"""
    query = select(Game).options(selectinload(Game.cards))
    result = await database.execute(query)
    return result.unique().scalars().all()


async def delete_game(database: AsyncSession, game: Game) -> None:
    """Deletes a game"""
    await database.delete(game)
    await database.commit()
