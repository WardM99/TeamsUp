"""Tests for a the crud actions of player"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.database.models import Player, Game, Team
from src.database.crud.player import (
                                      delete_player,
                                      create_player,
                                      get_player_by_id,
                                      get_player_by_name_and_password)
from src.database.crud.game import get_game
from src.database.crud.team import get_team

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
        player: Player = Player(name=f"Player{i}", password=f"Test{i}")
        database_session.add(player)

    await database_session.commit()

    return database_session


async def test_get_player_by_id(database_with_data: AsyncSession):
    """Test get_player_by_id"""
    player: Player = await get_player_by_id(database_with_data, 1)
    assert player.name == "Player1"
    assert player.password == "Test1"

    player: Player = await get_player_by_id(database_with_data, 2)
    assert player.name == "Player2"
    assert player.password == "Test2"

    player: Player = await get_player_by_id(database_with_data, 3)
    assert player.name == "Player3"
    assert player.password == "Test3"


async def test_get_player_by_id_ghost(database_with_data: AsyncSession):
    """Test get_player_by_id with an id that don't exist"""
    with pytest.raises(NoResultFound):
        await get_player_by_id(database_with_data, 1000)


async def test_create_player(database_with_data: AsyncSession):
    """Test create_player"""
    player_created: Player = await create_player(database_with_data, "New Player", "Monkey")
    assert player_created.name == "New Player"
    assert player_created.password == "Monkey"
    player: Player = await get_player_by_id(database_with_data, 4)
    assert player_created == player


async def test_create_player_same_name(database_with_data: AsyncSession):
    """Test to create a player with the same name"""
    player_created: Player = await create_player(database_with_data, "New Player", "Monkey")
    with pytest.raises(IntegrityError):
        player_created_copy: Player = await create_player(database_with_data, "New Player", "Monkey")


async def test_delete_player(database_with_data: AsyncSession):
    """Test to delete a player"""
    player: Player = await get_player_by_id(database_with_data, 3)
    assert player is not None
    await delete_player(database_with_data, player)
    with pytest.raises(NoResultFound):
        await get_player_by_id(database_with_data, 3)


async def test_get_player_by_name_and_password(database_with_data: AsyncSession):
    """Test to get a player by name and password"""
    player: Player = await get_player_by_name_and_password(database_with_data, "Player1", "Test1")
    assert player.name == "Player1"
    assert player.password == "Test1"


async def test_get_player_by_name_wrong_and_password(database_with_data: AsyncSession):
    """Test to get a player by name and password"""
    with pytest.raises(NoResultFound):
        player: Player = await get_player_by_name_and_password(database_with_data, "Payer1", "Test1")


async def test_get_player_by_name_and_password_wrong(database_with_data: AsyncSession):
    """Test to get a player by name and wrong password"""
    with pytest.raises(NoResultFound):
        player: Player = await get_player_by_name_and_password(database_with_data, "Player1", "Test2")
