"""Tests for a the crud actions of team"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from src.database.models import Game, Team
from src.database.crud.team import (
    create_team,
    get_team,
    get_all_teams_from_game
)
from src.database.crud.game import get_game

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

    return database_session


async def test_get_team(database_with_data: AsyncSession):
    """Test get_team"""
    game: Game = await get_game(database_with_data, 1)
    team1: Team = await get_team(database_with_data, 1, game)
    assert team1.team_id == 1
    assert team1.team_name == "Team1"
    team1: Team = await get_team(database_with_data, 2, game)
    assert team1.team_id == 2
    assert team1.team_name == "Team2"


async def test_get_team_wrong_game(database_with_data: AsyncSession):
    """Test that you don't get a team that isn't in the game"""
    game: Game = await get_game(database_with_data, 2)
    with pytest.raises(NoResultFound):
        await get_team(database_with_data, 1, game)


async def test_get_all_teams_from_game(database_with_data: AsyncSession):
    """Teast get_all_teams_from_game"""
    game1: Game = await get_game(database_with_data, 1)
    teams1: list[Team] = await get_all_teams_from_game(database_with_data, game1)
    assert len(teams1) == 2
    assert teams1[0].team_name == "Team1"
    assert teams1[1].team_name == "Team2"

    game2: Game = await get_game(database_with_data, 2)
    teams2: list[Team] = await get_all_teams_from_game(database_with_data, game2)
    assert len(teams2) == 1
    assert teams2[0].team_name == "Team3"


async def test_create_team(database_with_data: AsyncSession):
    """Test create a team"""
    game2: Game = await get_game(database_with_data, 2)
    team_new: Team = await create_team(database_with_data, "team4",game2)
    assert team_new.team_name == "team4"
    assert team_new.team_id == 4
    team: Team = await get_team(database_with_data, 4, game2)
    assert team == team_new
