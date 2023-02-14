"""Test app games"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from src.database.models import Game, Team, Player, Card
from src.database.crud.game import start_next_round
from tests.utils.authorization.auth_client import AuthClient


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
    
    team1: Team = Team(team_name="Team1", game = game)
    database_session.add(team1)
    await database_session.commit()

    await start_next_round(database_session, game)

    # Card
    for i in range(10):
        card: Card = Card(points=i, topic=f"Card{i}")
        database_session.add(card)
        game.cards.append(card)
    await database_session.commit()
    
    await start_next_round(database_session, game)

    return database_session

async def test_dont_get_guessed_card(database_with_data: AsyncSession, auth_client: AuthClient):
    """Test that I don't get a guessed card"""
    await auth_client.player()
    await auth_client.post("/games/1/teams/1")
    get_request = await auth_client.get("/games/1/cards")
    assert get_request.status_code == status.HTTP_200_OK
    card = get_request.json()
    post_request = await auth_client.post(f"/games/1/cards/{card['cardId']}")
    assert post_request.status_code == status.HTTP_200_OK
    for i in range(20):
        get_request = await auth_client.get("/games/1/cards")
        assert get_request.status_code == status.HTTP_200_OK
        assert get_request.json()["cardId"] is not card["cardId"]


async def test_dont_get_guessed_card_mutliple(database_with_data: AsyncSession, auth_client: AuthClient):
    """Test that I don't get multiple guessed cards"""
    await auth_client.player()
    await auth_client.post("/games/1/teams/1")
    for _ in range(3):
        get_request = await auth_client.get("/games/1/cards")
        assert get_request.status_code == status.HTTP_200_OK
        card = get_request.json()
        post_request = await auth_client.post(f"/games/1/cards/{card['cardId']}")
        assert post_request.status_code == status.HTTP_200_OK
        for _ in range(20):
            get_request = await auth_client.get("/games/1/cards")
            assert get_request.status_code == status.HTTP_200_OK
            assert get_request.json()["cardId"] is not card["cardId"]