"""Games routers"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.database import get_session
from src.app.logic.games import logic_get_all_games, logic_make_new_game, logic_get_game_by_id
from src.database.schemas.game import ReturnGames, ReturnGame
from src.database.models import Game
from src.app.routers.games.teams.teams import teams_router

games_router = APIRouter(prefix=("/games"))

games_router.include_router(teams_router, prefix="/{game_id}")

@games_router.get("", response_model=ReturnGames, status_code=status.HTTP_200_OK)
async def get_games(database: AsyncSession = Depends(get_session)):
    """Get all games"""
    games: list[Game] = await logic_get_all_games(database)

    return ReturnGames(games=games)


@games_router.post("", response_model=ReturnGame, status_code=status.HTTP_201_CREATED)
async def make_game(database: AsyncSession = Depends(get_session)):
    """Make a new game"""
    return await logic_make_new_game(database)


@games_router.get("/{game_id}", response_model=ReturnGame, status_code=status.HTTP_200_OK)
async def get_game(game_id: int, database: AsyncSession = Depends(get_session)):
    """Get a game by id"""
    return await logic_get_game_by_id(game_id, database)
 