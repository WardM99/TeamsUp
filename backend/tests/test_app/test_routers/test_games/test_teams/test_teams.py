"""Test app teams"""
#import pytest
#from sqlalchemy.ext.asyncio import AsyncSession
#from starlette import status
#from httpx import AsyncClient
#from src.database.models import Game, Team
#
#@pytest.fixture
#async def database_with_data(database_session: AsyncSession):
#    """A function to fill the database with fake data that can easly be used when testing"""
#    # Game
#    game1: Game = Game()
#    game2: Game = Game()
#    database_session.add(game1)
#    database_session.add(game2)
#    await database_session.commit()
#
#    # Team
#    team1: Team = Team(team_name="Team1", game = game1)
#    team2: Team = Team(team_name="Team2", game = game1)
#    team3: Team = Team(team_name="Team3", game = game2)
#
#    database_session.add(team1)
#    database_session.add(team2)
#    database_session.add(team3)
#    await database_session.commit()
#
#    return database_session
#
#async def test_get_all_teams_of_game(database_with_data: AsyncSession, test_client: AsyncClient):
#    """Test to get all teams of a game"""
#    get_request = await test_client.get("/games/1/teams")
#    assert get_request.status_code == status.HTTP_200_OK
#    data = get_request.json()
#    assert len(data["teams"]) == 2
#    for i in range(2):
#        team = data["teams"][i]
#        assert team["teamId"] == i+1
#        assert team["teamName"] == f"Team{i+1}"
#
#
#    get_request = await test_client.get("/games/2/teams")
#    assert get_request.status_code == status.HTTP_200_OK
#    data = get_request.json()
#    assert len(data["teams"]) == 1
#    team = data["teams"][0]
#    assert team["teamId"] == 3
#    assert team["teamName"] == "Team3"
#
#
#async def test_get_team_by_id(database_with_data: AsyncSession, test_client: AsyncClient):
#    """Test to get a team by id"""
#    get_request = await test_client.get("/games/1/teams/1")
#    assert get_request.status_code == status.HTTP_200_OK
#    data = get_request.json()
#    assert data["teamId"] == 1
#    assert data["teamName"] == "Team1"
#
#    get_request = await test_client.get("/games/1/teams/2")
#    assert get_request.status_code == status.HTTP_200_OK
#    data = get_request.json()
#    assert data["teamId"] == 2
#    assert data["teamName"] == "Team2"
#
#    get_request = await test_client.get("/games/2/teams/3")
#    assert get_request.status_code == status.HTTP_200_OK
#    data = get_request.json()
#    assert data["teamId"] == 3
#    assert data["teamName"] == "Team3"
#
#
#async def test_get_team_by_id_not_in_game(database_with_data: AsyncSession, test_client: AsyncClient):
#    """Test get team that is not in game"""
#    get_request = await test_client.get("/games/2/teams/1")
#    assert get_request.status_code == status.HTTP_404_NOT_FOUND
#    data = get_request.json()
#    assert data["message"] == "Not Found"
#
#
#async def test_add_team(database_with_data: AsyncSession, test_client: AsyncClient):
#    """Test to add a team to a game"""
#    post_request = await test_client.post("/games/2/teams", json={"team_name": "New Team"})
#    assert post_request.status_code == status.HTTP_201_CREATED
#    data = post_request.json()
#    assert data["teamName"] == "New Team"
#
#
#async def test_add_team_not_existing_game(database_with_data: AsyncSession, test_client: AsyncClient):
#    """Test to add a team to a not existing game"""
#    get_request = await test_client.get("/games/3")
#    assert get_request.status_code == status.HTTP_404_NOT_FOUND
#    assert get_request.json()["message"] == "Not Found"
#
#    post_request = await test_client.post("/games/3/teams", json={"teamName": "New Team"})
#    assert post_request.status_code == status.HTTP_404_NOT_FOUND
#    assert post_request.json()["message"] == "Not Found"
#