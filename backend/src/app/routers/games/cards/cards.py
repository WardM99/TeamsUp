"""Cards routers"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.database import get_session
from src.app.logic.players import require_player
from src.app.logic.games import logic_get_game_by_id
from src.app.logic.cards import logic_add_card_to_game, logic_get_random_card, logic_update_card
from src.database.models import Game, Player, Card
from src.database.schemas.card import InputCard

card_router = APIRouter(prefix="/cards")

@card_router.get("", dependencies=[Depends(require_player)])
async def get_next_card(
                        database: AsyncSession = Depends(get_session),
                        game: Game = Depends(logic_get_game_by_id)
                        ):
    """Get next card"""
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
                       game: Game = Depends(logic_get_game_by_id)):
    """Card is guessed correctly"""
    await logic_update_card(database, game, card_id)


@card_router.patch("/{card_id}")
async def overrule_previous_card(card_id: int,
                       database: AsyncSession = Depends(get_session),
                       game: Game = Depends(logic_get_game_by_id)):
    """Overrule the previous card when selected wrongly"""
    await logic_update_card(database, game, card_id)
