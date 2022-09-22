"""Test app teams"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from httpx import AsyncClient
from src.database.models import Game, Team, Player

@pytest.fixture
async def database_with_data(database_session: AsyncSession):
    """A function to fill the database with fake data that can easly be used when testing"""
    # Game
    game1: Game = Game()
    game2: Game = Game()
    database_session.add(game1)
    database_session.add(game2)
    await database_session.commit()

    # Team
    team1: Team = Team(team_name="Team1", game = game1)
    team2: Team = Team(team_name="Team2", game = game1)
    team3: Team = Team(team_name="Team3", game = game2)

    database_session.add(team1)
    database_session.add(team2)
    database_session.add(team3)
    await database_session.commit()

    # Player
    for i in range(1,4):
        player1: Player = Player(name=f"Team1Player{i}", team=team1)
        player2: Player = Player(name=f"Team2Player{i}", team=team2)
        database_session.add(player1)
        database_session.add(player2)

    await database_session.commit()

    return database_session


async def test_get_all_players_of_teams(database_with_data: AsyncSession, test_client: AsyncClient):
    """Test to get all the players of a team"""
    get_request = await test_client.get("/games/1/teams/1/players")
    assert get_request.status_code == status.HTTP_200_OK
    data = get_request.json()
    assert len(data["players"]) == 3
    for i in range(1,4):
        player = data["players"][i-1]
        assert player["name"] == f"Team1Player{i}"

    get_request = await test_client.get("/games/1/teams/2/players")
    assert get_request.status_code == status.HTTP_200_OK
    data = get_request.json()
    assert len(data["players"]) == 3
    for i in range(1,4):
        player = data["players"][i-1]
        assert player["name"] == f"Team2Player{i}"


async def test_get_player_by_id(database_with_data: AsyncSession, test_client: AsyncClient):
    """Test to get a player by id"""
    get_request = await test_client.get("/games/1/teams/1/players/1")
    assert get_request.status_code == status.HTTP_200_OK
    data = get_request.json()
    assert data["name"] == "Team1Player1"

    get_request = await test_client.get("/games/1/teams/2/players/2")
    assert get_request.status_code == status.HTTP_200_OK
    data = get_request.json()
    assert data["name"] == "Team2Player1"


async def test_get_player_by_id_not_in_team(database_with_data: AsyncSession, test_client: AsyncClient):
    """Test to get a player that is not in that team"""
    get_request = await test_client.get("/games/1/teams/2/players/1")
    assert get_request.status_code == status.HTTP_404_NOT_FOUND
    data = get_request.json()
    assert data["message"] == "Not Found"


async def test_get_player_by_id_that_dont_exist(database_with_data: AsyncSession, test_client: AsyncClient):
    """Test to get a player that don't exist"""
    get_request = await test_client.get("/games/1/teams/1/players/1000")
    assert get_request.status_code == status.HTTP_404_NOT_FOUND
    data = get_request.json()
    assert data["message"] == "Not Found"


async def test_add_player_to_team(database_with_data: AsyncSession, test_client: AsyncClient):
    """Test to add a player to a team"""
    post_request = await test_client.post("/games/2/teams/3/players", json={"name": "New Player"})
    assert post_request.status_code == status.HTTP_201_CREATED
    data = post_request.json()
    assert data["player"]["name"] == "New Player"

async def test_add_player_to_dont_existing_team(database_with_data: AsyncSession, test_client: AsyncClient):
    """Test to add a player to a team that don't exist"""
    post_request = await test_client.post("/games/2/teams/4/players", json={"name": "New Player"})
    assert post_request.status_code == status.HTTP_404_NOT_FOUND
    data = post_request.json()
    assert data["message"] == "Not Found"
