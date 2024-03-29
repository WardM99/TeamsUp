"""Logic of cards route"""
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Game, Card
from src.database.crud.card import (get_card_by_id,
                                    add_card_to_game,
                                    get_random_card,
                                    update_card,
                                    reset_cards_game,
                                    add_cards_to_database,
                                    get_cards)

async def logic_add_card_to_game(database: AsyncSession, game: Game, card_id: int) -> None:
    """Logic to add a card to a game"""
    if game.may_suggests_cards:
        card: Card = await get_card_by_id(database, card_id)
        await add_card_to_game(database, card, game)


async def logic_get_random_card(database: AsyncSession, game: Game) -> Card:
    """Logic to get a random card"""
    return await get_random_card(database, game)


async def logic_update_card(database: AsyncSession, game: Game, card_id: int) -> None:
    """Logic to update a card"""
    card: Card = await get_card_by_id(database, card_id)
    await update_card(database, game, card)


async def logic_reset_cards(database: AsyncSession, game: Game) -> None:
    """Logic to reset all cards of a game"""
    await reset_cards_game(database, game)


async def logic_add_cards_to_database(database: AsyncSession) -> None:
    """Logic to add cards to database"""
    await add_cards_to_database(database)


async def logic_get_cards(database: AsyncSession) -> list[Card]:
    """Logic to get all cards"""
    return await get_cards(database)
