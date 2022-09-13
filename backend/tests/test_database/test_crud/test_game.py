"""Tests for a the crud actions of game"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Game
from src.database.crud.game import get_game
from tests.conftest import database_session

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
    game: Game = get_game(database_with_data, 1)
    print(game)
