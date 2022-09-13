"""Tests for a the crud actions of player"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Player, Game, Team
from src.database.crud.player import get_player
from tests.conftest import database_session

@pytest.fixture
async def database_with_data(database_session: AsyncSession):
    """A function to fill the database with fake data that can easly be used when testing"""
    # Game
    game: Game = Game(round_one_done = True)
    database_session.add(game)
    await database_session.commit()

    # Team
    #team1: Team = Team(team_name="Team1", game = game)
    #team2: Team = Team(team_name="Team2", game = game)

    #database_session.add(team1)
    #database_session.add(team2)
    #await database_session.commit()

    # Player
    #for i in range(1,4):
    #    player1: Player = Player(name=f"Team1Player{i}", team=team1)
    #    player2: Player = Player(name=f"Team2Player{i}", team=team2)
    #    database_session.add(player1)
    #    database_session.add(player2)

    #await database_session.commit()


#async def test_get_player(database_with_data: AsyncSession):
#    """test get player"""
#    player: Player = get_player(database_with_data, 1)
#    assert player.player_id == 1
#    assert player.name == "Team1Player1"
