"""Tests for a the crud actions of game"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Game
from src.database.crud.game import (
    get_all_games,
    get_game,
    create_game
)

@pytest.fixture
async def database_with_data(database_session: AsyncSession):
    """A function to fill the database with fake data that can easly be used when testing"""
    # Game
    game: Game = Game()
    database_session.add(game)
    await database_session.commit()

    return database_session


async def test_get_game(database_with_data: AsyncSession):
    """Test get_game"""
    game: Game = await get_game(database_with_data, 1)
    assert game.game_id == 1
    assert game.round_one_done is False
    assert game.round_two_done is False
    assert game.round_three_done is False


async def test_get_all_games(database_with_data: AsyncSession):
    """Test get_all_games"""
    games: list[Game] = await get_all_games(database_with_data)
    assert len(games) == 1


async def test_create_game(database_with_data: AsyncSession):
    """test create_game"""
    game_new: Game = await create_game(database_with_data)
    games: list[Game] = await get_all_games(database_with_data)
    assert len(games) == 2
    game: Game = await get_game(database_with_data, 2)
    assert game.game_id == game_new.game_id
    assert game.round_one_done is game_new.round_one_done
    assert game.round_two_done is game_new.round_two_done
    assert game.round_three_done is game_new.round_three_done
