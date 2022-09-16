"""Test app"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from src.database.models import Game

@pytest.fixture
async def database_with_data(database_session: AsyncSession):
    """A function to fill the database with fake data that can easly be used when testing"""
    # Game
    game: Game = Game()
    database_session.add(game)
    await database_session.commit()

    return database_session


async def test_app_hello_world(database_with_data: AsyncSession, test_client: AsyncClient):
    """Test hello world"""
    get_request = await test_client.get("")
    data = get_request.json()
    assert data["message"] == "Hello World"
