"""Tests for a the crud actions of card"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.models import Card, Game, Player, card_games
from src.database.crud.card import (
    get_random_card, update_card, reset_cards_game
)
from src.database.crud.game import get_game

@pytest.fixture
async def database_with_data(database_session: AsyncSession):
    """A function to fill the database with fake data that can easly be used when testing"""
     # Player
    player: Player = Player(name="Joske", password="Test")
    database_session.add(player)
    await database_session.commit()

    # Game
    game: Game = Game(owner=player, cards = [])
    database_session.add(game)
    await database_session.commit()

    # Card
    for i in range(10):
        card: Card = Card(points=i, topic=f"Card{i}")
        database_session.add(card)
        game.cards.append(card)
    await database_session.commit()

    return database_session


async def test_get_random_card(database_with_data: AsyncSession):
    """To get a card from the game that isn't guessed"""
    game = await get_game(database_with_data, 1)
    for _ in range(4):
        card = await get_random_card(database_with_data, game)
        await update_card(database_with_data, game, card)
    query = select(card_games.columns.card_id).where(card_games.columns.game_id == game.game_id).where(card_games.columns.guessed == False)
    result = await database_with_data.execute(query)
    value = result.unique().scalars().all()
    assert len(value) == 6

    await reset_cards_game(database_with_data, game)
    query = select(card_games.columns.card_id).where(card_games.columns.game_id == game.game_id).where(card_games.columns.guessed == False)
    result = await database_with_data.execute(query)
    value = result.unique().scalars().all()
    assert len(value) == 10
