"""Tests for a the crud actions of card"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.models import Card, Game, Player, card_games
from src.database.crud.card import (
    get_random_card, update_card, reset_cards_game, add_card_to_game, get_unguessed_cards,
    get_cards
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
    unguessed_cards: list[Card] = await get_unguessed_cards(database_with_data, game)
    assert len(unguessed_cards) == 10
    for _ in range(4):
        card = await get_random_card(database_with_data, game)
        await update_card(database_with_data, game, card)
    
    unguessed_cards: list[Card] = await get_unguessed_cards(database_with_data, game)
    assert len(unguessed_cards) == 6

    await reset_cards_game(database_with_data, game)
    unguessed_cards: list[Card] = await get_unguessed_cards(database_with_data, game)
    assert len(unguessed_cards) == 10


async def test_add_card_to_game(database_with_data: AsyncSession):
    """Test to add a card to a game"""
    game = await get_game(database_with_data, 1)
    query = select(card_games.columns.card_id).where(card_games.columns.game_id == game.game_id)
    result = await database_with_data.execute(query)
    value = result.unique().scalars().all()
    assert len(value) == 10

    card: Card = Card(points=5, topic="New card")
    database_with_data.add(card)
    await database_with_data.commit()
    await add_card_to_game(database_with_data, card, game)

    query = select(card_games.columns.card_id).where(card_games.columns.game_id == game.game_id)
    result = await database_with_data.execute(query)
    value = result.unique().scalars().all()
    assert len(value) == 11


async def test_add_multiple_cards_to_game(database_with_data: AsyncSession):
    """Test to add multiple cards to a game"""
    game = await get_game(database_with_data, 1)
    query = select(card_games.columns.card_id).where(card_games.columns.game_id == game.game_id)
    result = await database_with_data.execute(query)
    value = result.unique().scalars().all()
    assert len(value) == 10

    card1: Card = Card(points=5, topic="New card1")
    card2: Card = Card(points=30, topic="New card2")
    database_with_data.add(card1)
    database_with_data.add(card2)
    await database_with_data.commit()

    await add_card_to_game(database_with_data, card1, game)
    await add_card_to_game(database_with_data, card2, game)

    query = select(card_games.columns.card_id).where(card_games.columns.game_id == game.game_id)
    result = await database_with_data.execute(query)
    value = result.unique().scalars().all()
    assert len(value) == 12


async def test_get_unguessed_cards(database_with_data: AsyncSession):
    """Test to get all the unguessed cards"""
    game = await get_game(database_with_data, 1)
    cards = await get_unguessed_cards(database_with_data, game)
    assert len(cards) == 10
    for _ in range(9):
        card = await get_random_card(database_with_data, game)
        await update_card(database_with_data, game, card)
    cards = await get_unguessed_cards(database_with_data, game)
    assert len(cards) == 1


async def test_get_cards(database_with_data: AsyncSession):
    """Test to get cards"""
    cards: list[Card] = await get_cards(database_with_data)
    assert len(cards) == 10
