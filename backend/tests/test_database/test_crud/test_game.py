"""Tests for a the crud actions of game"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from src.database.models import Game, Player
from src.database.crud.game import (
    get_all_games,
    get_game,
    create_game,
    delete_game,
    start_suggests_cards,
    start_next_round
)

@pytest.fixture
async def database_with_data(database_session: AsyncSession):
    """A function to fill the database with fake data that can easly be used when testing"""
    # Player
    player: Player = Player(name="Joske", password="Test")
    database_session.add(player)
    await database_session.commit()

    # Game
    game: Game = Game(owner=player)
    database_session.add(game)
    await database_session.commit()

    return database_session


async def test_get_game(database_with_data: AsyncSession):
    """Test get_game"""
    game: Game = await get_game(database_with_data, 1)
    assert game.game_id == 1
    assert game.round_one_done is False
    assert game.round_two_done is False
    assert game.round_three_done is False


async def test_get_game_no_game(database_with_data: AsyncSession):
    """Test get error when no games found"""
    with pytest.raises(NoResultFound):
        await get_game(database_with_data, 2)


async def test_get_all_games(database_with_data: AsyncSession):
    """Test get_all_games"""
    games: list[Game] = await get_all_games(database_with_data)
    assert len(games) == 1


async def test_create_game(database_with_data: AsyncSession):
    """test create_game"""
    player: Player = Player(name="Testeron", password="Test")
    game_new: Game = await create_game(database_with_data, player)
    games: list[Game] = await get_all_games(database_with_data)
    assert len(games) == 2
    game: Game = await get_game(database_with_data, 2)
    assert game.game_id == game_new.game_id
    assert game.round_one_done is game_new.round_one_done
    assert game.round_two_done is game_new.round_two_done
    assert game.round_three_done is game_new.round_three_done
    assert game.owner_id == player.player_id


async def test_delete_team(database_with_data: AsyncSession):
    """Test delete_player"""
    game: Game = await get_game(database_with_data, 1)
    await delete_game(database_with_data, game)
    with pytest.raises(NoResultFound):
        await get_game(database_with_data, 1)


async def test_start_suggest_cards(database_with_data: AsyncSession):
    """Test to start may suggesting cards"""
    game: Game = await get_game(database_with_data, 1)
    assert not game.may_suggests_cards

    await start_suggests_cards(database_with_data, game)
    assert game.may_suggests_cards


async def test_start_next_round(database_with_data: AsyncSession):
    """Test to start the next round"""
    game: Game = await get_game(database_with_data, 1)
    assert not game.round_one_done
    assert not game.round_two_done
    assert not game.round_three_done

    await start_next_round(database_with_data, game)
    assert game.round_one_done
    assert not game.round_two_done
    assert not game.round_three_done

    await start_next_round(database_with_data, game)
    assert game.round_one_done
    assert game.round_two_done
    assert not game.round_three_done

    await start_next_round(database_with_data, game)
    assert game.round_one_done
    assert game.round_two_done
    assert game.round_three_done
