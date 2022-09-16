"""Tests for a the crud actions of player"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from src.database.models import Player, Game, Team
from src.database.crud.player import (get_player,
                                      get_players_game,
                                      get_players_team,
                                      delete_player)
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
        player1: Player = Player(name=f"Team1Player{i}", team=team1)
        player2: Player = Player(name=f"Team2Player{i}", team=team2)
        database_session.add(player1)
        database_session.add(player2)

    await database_session.commit()

    return database_session


async def test_get_player(database_with_data: AsyncSession):
    """Test get_player"""
    game: Game = await get_game(database_with_data, 1)
    team1: Team = await get_team(database_with_data, 1, game)
    team2: Team = await get_team(database_with_data, 2, game)
    player: Player = await get_player(database_with_data, 1, team1)
    assert player.name == "Team1Player1"
    player: Player = await get_player(database_with_data, 2, team2)
    assert player.name == "Team2Player1"


async def test_get_player_not_in_team(database_with_data: AsyncSession):
    """Test get_player when player is not in the team"""
    game: Game = await get_game(database_with_data, 1)
    team2: Team = await get_team(database_with_data, 2, game)
    with pytest.raises(NoResultFound):
        await get_player(database_with_data, 1, team2)


async def test_get_players_game(database_with_data: AsyncSession):
    """test get_players_game"""
    game: Game = await get_game(database_with_data, 1)
    players: list[Player] = await get_players_game(database_with_data, game)
    assert len(players) == 6


async def test_get_players_team(database_with_data: AsyncSession):
    """Test get_players_team"""
    game: Game = await get_game(database_with_data, 1)
    team1: Team = await get_team(database_with_data, 1, game)
    team2: Team = await get_team(database_with_data, 2, game)
    players_team1 = await get_players_team(database_with_data, team1)
    players_team2 = await get_players_team(database_with_data, team2)
    assert len(players_team1) == 3
    assert len(players_team2) == 3


async def test_delete_player(database_with_data: AsyncSession):
    game: Game = await get_game(database_with_data, 1)
    team1: Team = await get_team(database_with_data, 1, game)
    player: Player = await get_player(database_with_data, 5, team1)
    await delete_player(database_with_data, player)
    with pytest.raises(NoResultFound):
        await get_player(database_with_data, 5, team1)
