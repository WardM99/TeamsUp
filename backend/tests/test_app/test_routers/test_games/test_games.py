"""Test app games"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from httpx import AsyncClient
from src.database.models import Game

@pytest.fixture
async def database_with_data(database_session: AsyncSession):
    """A function to fill the database with fake data that can easly be used when testing"""
    # Game
    game1: Game = Game()
    game2: Game = Game()
    database_session.add(game1)
    database_session.add(game2)
    await database_session.commit()

    return database_session


async def test_get_all_games(database_with_data: AsyncSession, test_client: AsyncClient):
    """Test get all games"""
    get_request = await test_client.get("/games")
    data = get_request.json()
    print(data)
    assert get_request.status_code == status.HTTP_200_OK
    assert len(data["games"]) == 2
    for i in range(2):
        game = data["games"][i]
        assert game["gameId"] == i + 1
        assert not game["roundOneDone"]
        assert not game["roundTwoDone"]
        assert not game["roundThreeDone"]
