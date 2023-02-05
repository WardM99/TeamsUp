"""Games routers"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.database import get_session
from src.app.logic.games import (logic_get_all_games,
                                 logic_make_new_game,
                                 logic_get_your_turn,
                                 logic_get_game_by_id,
                                 logic_next_round)
from src.app.logic.players import require_player
from src.database.schemas.game import ReturnGames, ReturnGame, ReturnTurn, ReturnGameStatus
from src.database.models import Player, Game

from src.app.routers.games.teams.teams import teams_router
from src.app.routers.games.cards.cards import card_router

games_router = APIRouter(prefix="/games")

games_router.include_router(teams_router, prefix="/{game_id}")
games_router.include_router(card_router, prefix="/{game_id}")

@games_router.get("", response_model=ReturnGames,
                  status_code=status.HTTP_200_OK,
                  dependencies=[Depends(require_player)])
async def get_games(database: AsyncSession = Depends(get_session)):
    """Get all games"""
    return await logic_get_all_games(database)


@games_router.post("", response_model=ReturnGame, status_code=status.HTTP_201_CREATED)
async def make_game(database: AsyncSession = Depends(get_session),
                    owner: Player = Depends(require_player)):
    """Make a new game"""
    return await logic_make_new_game(database, owner)


@games_router.get("/stream")
async def stream_view():
    """Get the stream view"""
    return {"details": "Not Implemented"}


@games_router.get("/{game_id}/myturn", response_model=ReturnTurn)
async def my_turn(game_id: int, database:AsyncSession = Depends(get_session),
                  player: Player = Depends(require_player)):
    """To check if it's your turn or not"""
    turn: bool = await logic_get_your_turn(database, game_id, player)
    return ReturnTurn(your_turn=turn)


@games_router.patch("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
async def next_status(database: AsyncSession = Depends(get_session),
                      game: Game = Depends(logic_get_game_by_id),
                      player: Player = Depends(require_player)):
    """Goes to the next round"""
    await logic_next_round(database, game, player)


@games_router.get("/{game_id}", status_code=status.HTTP_200_OK, response_model=ReturnGameStatus)
async def get_game_status(game_id: int, database: AsyncSession = Depends(get_session)):
    """Gives the game status"""
    game: Game = await logic_get_game_by_id(game_id, database)
    return game
