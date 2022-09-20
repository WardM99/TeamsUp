"""Logic of games route"""
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.crud.game import get_all_games, create_game, get_game
from src.database.models import Game


async def logic_get_all_games(database: AsyncSession) -> list[Game]:
    """The logic to get all games"""
    return await get_all_games(database)


async def logic_make_new_game(database: AsyncSession) -> Game:
    """The logic to create a new game"""
    return await create_game(database)


async def logic_get_game_by_id(database: AsyncSession, game_id: int) -> Game:
    """The logic to get a game by id"""
    return await get_game(database, game_id)
