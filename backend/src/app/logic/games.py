"""Logic of games route"""
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.crud.game import get_all_games
from src.database.models import Game


async def logic_get_all_games(database: AsyncSession) -> list[Game]:
    """The logic to get all games"""
    return await get_all_games(database)
