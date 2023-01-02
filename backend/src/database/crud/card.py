"""all crud operations for a card"""
# pylint: disable=C0121
from random import choice
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Card, Game, card_games


async def get_card_by_id(database: AsyncSession, card_id: int) -> Card:
    """Returns a card"""
    query = select(Card).where(Card.card_id == card_id)
    result = await database.execute(query)
    return result.unique().scalars().one()


async def add_card_to_game(database: AsyncSession, card: Card, game: Game) -> None:
    """Adds a card to a game"""
    game.cards.append(card)
    await database.commit()


async def get_random_card(database: AsyncSession, game: Game)-> Card:
    """Get a random card that isn't guessed"""
    query = select(card_games.columns.card_id)\
        .where(card_games.columns.game_id == game.game_id)\
        .where(card_games.columns.guessed == False)
    result = await database.execute(query)
    card_ids = result.unique().scalars().all()
    return await get_card_by_id(database, choice(card_ids))


async def update_card(database: AsyncSession, game: Game, card: Card) -> None:
    """Update a specific card to the opposite value"""
    query_select = select(card_games.columns.guessed)\
        .where(card_games.columns.game_id == game.game_id)\
        .where(card_games.columns.card_id == card.card_id)
    result = await database.execute(query_select)
    value = result.unique().scalars().one()
    query_update = update(card_games)\
            .where(card_games.columns.card_id == card.card_id)\
            .where(card_games.columns.game_id == game.game_id)\
            .values(guessed = not value)
    await database.execute(query_update)


async def reset_cards_game(database: AsyncSession, game: Game) -> None:
    """Update all cards to it's started value"""
    query = update(card_games)\
            .where(card_games.columns.game_id == game.game_id)\
            .values(guessed = False)
    await database.execute(query)


async def get_unguessed_cards(database: AsyncSession, game: Game) -> list[Card]:
    """get all cards that are unguessed"""
    query = select(card_games.columns.card_id)\
        .where(card_games.columns.game_id == game.game_id)\
        .where(card_games.columns.guessed == False)
    result = await database.execute(query)
    value = result.unique().scalars().all()
    return value
