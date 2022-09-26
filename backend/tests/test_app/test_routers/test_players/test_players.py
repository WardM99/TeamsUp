"""Test app players"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from tests.utils.authorization.auth_client import AuthClient
from src.database.models import Game, Player


async def test_new_player(database_session: AsyncSession, auth_client: AuthClient):
    """Test to make a new player"""
    post_request = await auth_client.post("/players", json={"name": "New Player", "password": "Wachtwoord"})
    assert post_request.status_code == status.HTTP_201_CREATED
    data = post_request.json()
    assert data["player"]["playerId"] == 1
    assert data["player"]["name"] == "New Player"


async def test_duplicate_player(database_session: AsyncSession, auth_client: AuthClient):
    """Test add a duplicate player"""
    post_request = await auth_client.post("/players", json={"name": "New Player", "password": "Wachtwoord"})
    assert post_request.status_code == status.HTTP_201_CREATED
    post_request = await auth_client.post("/players", json={"name": "New Player", "password": "Wachtwoord"})
    assert post_request.status_code == status.HTTP_400_BAD_REQUEST
    assert post_request.json()["detail"] == "Bad Request"


async def test_current_player(database_session: AsyncSession, auth_client: AuthClient):
    """Test get current player"""
    await auth_client.player()
    get_request = await auth_client.get("/players/current")
    assert get_request.status_code == status.HTTP_200_OK
    assert get_request.json()["name"] == "Player1"
