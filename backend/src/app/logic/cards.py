"""Logic of cards route"""
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Game, Card
from src.database.crud.card import get_card_by_id, add_card_to_game

async def logic_add_card_to_game(database: AsyncSession, game: Game, card_id: Card) -> None:
    """Logic to add a card to a game"""
    card: Card = await get_card_by_id(database, card_id)
    await add_card_to_game(database, card, game)
