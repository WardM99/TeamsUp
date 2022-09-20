"""Games routers"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.database import get_session
from src.app.logic.games import logic_get_all_games
from src.database.schemas.game import ReturnGames
from src.database.models import Game

games_router = APIRouter(prefix=("/games"))

@games_router.get("", response_model=ReturnGames, status_code=status.HTTP_200_OK)
async def get_game(database: AsyncSession = Depends(get_session)):
    """Get all games"""
    games: list[Game] = await logic_get_all_games(database)

    return ReturnGames(games=games)
