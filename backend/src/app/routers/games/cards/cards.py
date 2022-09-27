"""Cards routers"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.database import get_session
from src.app.logic.players import require_player
from src.app.logic.games import logic_get_game_by_id, logic_get_your_turn
from src.app.logic.cards import logic_add_card_to_game, logic_get_random_card, logic_update_card
from src.database.models import Game, Player
from src.database.schemas.card import InputCard

card_router = APIRouter(prefix="/cards")

@card_router.get("")
async def get_next_card(
                        database: AsyncSession = Depends(get_session),
                        game: Game = Depends(logic_get_game_by_id),
                        player: Player = Depends(require_player)
                        ):
    """Get next card"""
    if await logic_get_your_turn(database, game.game_id, player):
        return await logic_get_random_card(database, game)


@card_router.post("", dependencies=[Depends(require_player)], status_code=status.HTTP_204_NO_CONTENT)
async def add_card(input_card: InputCard,
                   database: AsyncSession = Depends(get_session),
                   game: Game = Depends(logic_get_game_by_id)):
    """Add a card to game"""
    await logic_add_card_to_game(database, game, input_card.card_id)


@card_router.post("/{card_id}", dependencies=[Depends(require_player)])
async def correct_card(card_id: int,
                       database: AsyncSession = Depends(get_session),
                       game: Game = Depends(logic_get_game_by_id),
                       player: Player = Depends(require_player)):
    """Card is guessed correctly"""
    if await logic_get_your_turn(database, game.game_id, player):
        await logic_update_card(database, game, card_id)


@card_router.patch("/{card_id}")
async def overrule_previous_card(card_id: int,
                                 database: AsyncSession = Depends(get_session),
                                 game: Game = Depends(logic_get_game_by_id),
                                 player: Player = Depends(require_player)):
    """Overrule the previous card when selected wrongly"""
    if game.owner == player:
        await logic_update_card(database, game, card_id)
