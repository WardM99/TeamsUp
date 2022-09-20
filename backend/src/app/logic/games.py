"""Logic of games route"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_session
from src.database.crud.game import get_all_games, create_game, get_game
from src.database.models import Game


async def logic_get_all_games(database: AsyncSession) -> list[Game]:
    """The logic to get all games"""
    return await get_all_games(database)


async def logic_make_new_game(database: AsyncSession) -> Game:
    """The logic to create a new game"""
    return await create_game(database)


async def logic_get_game_by_id(game_id: int, database: AsyncSession = Depends(get_session)) -> Game:
    """The logic to get a game by id"""
    return await get_game(database, game_id)
