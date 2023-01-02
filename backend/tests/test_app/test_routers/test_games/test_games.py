"""Test app games"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from tests.utils.authorization.auth_client import AuthClient
from src.database.crud.team import create_team,add_player
from src.database.models import Game, Player, Team

@pytest.fixture
async def database_with_data(database_session: AsyncSession):
    """A function to fill the database with fake data that can easly be used when testing"""
    # Player
    player: Player = Player(name="Joske", password="Test")
    database_session.add(player)
    await database_session.commit()

    # Game
    game1: Game = Game(owner = player)
    game2: Game = Game(owner = player)
    database_session.add(game1)
    database_session.add(game2)
    await database_session.commit()
    team: Team = await create_team(database_session, "Team1", game1)
    await create_team(database_session, "Team2", game1)
    await create_team(database_session, "Team3", game2)
    await create_team(database_session, "Team4", game2)
    await add_player(database_session, team,player)


    return database_session


async def test_get_all_games(database_with_data: AsyncSession, auth_client: AuthClient):
    """Test get all games"""
    await auth_client.player()
    get_request = await auth_client.get("/games")
    assert get_request.status_code == status.HTTP_200_OK
    data = get_request.json()
    assert len(data["games"]) == 2
    for i in range(2):
        game = data["games"][i]
        assert game["gameId"] == i + 1
        assert not game["roundOneDone"]
        assert not game["roundTwoDone"]
        assert not game["roundThreeDone"]


async def test_make_a_new_game(database_with_data: AsyncSession, auth_client: AuthClient):
    """Test to make a new game"""
    await auth_client.player()
    post_request = await auth_client.post("/games")
    assert post_request.status_code == status.HTTP_201_CREATED
    data = post_request.json()
    assert data["gameId"] == 3
    assert not data["roundOneDone"]
    assert not data["roundTwoDone"]
    assert not data["roundThreeDone"]
    assert data["owner"]["name"] == "Player1"


async def test_my_turn(database_with_data: AsyncSession, auth_client: AuthClient):
    """Test if it's your turn"""
    await auth_client.player()
    post_request = await auth_client.post("/games/1/teams/1")
    assert post_request.status_code == status.HTTP_200_OK

    my_turn_request = await auth_client.get("/games/1/myturn")
    assert my_turn_request.status_code == status.HTTP_200_OK
    data = my_turn_request.json()
    assert not data["yourTurn"]
    
    post_request = await auth_client.post("/games/2/teams/3")
    assert post_request.status_code == status.HTTP_200_OK
    my_turn_request = await auth_client.get("/games/2/myturn")
    assert my_turn_request.status_code == status.HTTP_200_OK
    data = my_turn_request.json()
    assert data["yourTurn"]
