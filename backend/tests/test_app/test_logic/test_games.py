"""Tests for the logic of games route"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.crud.card import get_unguessed_cards
from src.database.crud.game import get_game
from src.database.crud.team import create_team,add_player, get_team
from src.database.models import Player, Game, Team, Card
from src.app.logic.cards import logic_add_card_to_game
from src.app.logic.games import (
    logic_get_all_games,
    logic_make_new_game,
    logic_get_game_by_id,
    logic_get_your_turn,
    logic_next_round,
)
from src.app.exceptions.wrongplayer import WrongPlayerException

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
    await add_player(database_session, team, player)

    return database_session


async def test_logic_get_all_games(database_with_data: AsyncSession):
    """Test the logic_get_all_games function"""
    all_games = await logic_get_all_games(database_with_data)
    assert len(all_games.games) == 2


async def test_logic_make_new_game(database_with_data: AsyncSession):
    """Test the logic_make_new_game function"""
    owner = Player(name="testuser", password="test")
    game = await logic_make_new_game(database_with_data, owner)
    assert game.owner.player_id == owner.player_id
    assert game.owner.name == owner.name


async def test_logic_get_game_by_id(database_with_data: AsyncSession):
    """Test the logic_get_game_by_id function"""
    owner = Player(name="testuser", password="test")
    database_with_data.add(owner)
    await database_with_data.commit()
    game = await logic_make_new_game(database_with_data, owner)
    fetched_game = await logic_get_game_by_id(game.game_id, database_with_data)
    assert fetched_game.game_id == game.game_id


async def test_logic_get_your_turn(database_with_data: AsyncSession):
    """Test the logic_get_your_turn function"""
    player: Player = Player(name="J", password="W")
    database_with_data.add(player)
    await database_with_data.commit()
    game: Game = await get_game(database_with_data, 1)
    team: Team = await get_team(database_with_data, 2, game)
    await add_player(database_with_data, team, player)

    
    myturn = await logic_get_your_turn(database_with_data, game.game_id, player)
    assert myturn is False

    game: Game = await get_game(database_with_data, 2)
    team: Team = await get_team(database_with_data, 3, game)
    await add_player(database_with_data, team, player)
    myturn = await logic_get_your_turn(database_with_data, game.game_id, player)
    assert myturn is True

################### CHAT GPT ##################################

async def test_logic_next_round(database_with_data: AsyncSession):
    """Test the logic_next_round function"""
    owner = Player(name="testuser", password="test")
    database_with_data.add(owner)
    await database_with_data.commit()
    game = await logic_make_new_game(database_with_data, owner)
    await logic_next_round(database_with_data, game, owner)
    assert game.may_suggests_cards


async def test_logic_next_round_zero_cards(database_with_data: AsyncSession):
    """Test the logic_next_round function when there are zero cards left"""
    owner = Player(name="testuser", password="test")
    database_with_data.add(owner)
    await database_with_data.commit()
    game: Game = await get_game(database_with_data, 1)
    cards = await get_unguessed_cards(database_with_data, game)
    for card in cards:
        card.guessed = True
        database_with_data.add(card)
    await database_with_data.commit()
    with pytest.raises(WrongPlayerException):
        await logic_next_round(database_with_data, game, owner)


async def test_logic_next_round_start_game(database_with_data: AsyncSession):
    """Test the logic_next_round function when starting the game"""
    owner: Player = Player(name="testuser", password="test")
    database_with_data.add(owner)
    await database_with_data.commit()
    new_game = await logic_make_new_game(database_with_data, owner)

    game: Game = await logic_get_game_by_id(new_game.game_id, database_with_data)
    
    await logic_next_round(database_with_data, game, owner)
    assert game.may_suggests_cards
    topics = [
        "astronomy",
        "telephone",
        "astronomy",
        "royalty",
        "monkeys",
        "pipe organs",
        "pilots",
        "football",
        "volcanoes",
    ]
    for topic in topics:
        card: Card = Card(points=10, topic=topic)
        database_with_data.add(card)
        await database_with_data.commit()
        await logic_add_card_to_game(database_with_data, game, card.card_id)
    assert not game.game_started
    await logic_next_round(database_with_data, game, owner)
    assert game.game_started


async def test_logic_next_round_non_owner_player(database_with_data: AsyncSession):
    """Test the logic_next_round function when a non-owner player tries to go to the next round"""
    owner = Player(name="testuser", password="test")
    database_with_data.add(owner)
    await database_with_data.commit()
    game = await logic_make_new_game(database_with_data, owner)
    player = Player(name="testuser2", password="test")
    database_with_data.add(player)
    await database_with_data.commit()
    with pytest.raises(WrongPlayerException):
        await logic_next_round(database_with_data, game, player)


async def test_logic_next_round_not_your_turn(database_with_data: AsyncSession):
    """Test the logic_next_round function when it's not the player's turn"""
    owner: Player = Player(name="testuser", password="test")
    database_with_data.add(owner)
    await database_with_data.commit()
    new_game = await logic_make_new_game(database_with_data, owner)
    game: Game = await logic_get_game_by_id(new_game.game_id, database_with_data)
    
    
    team1: Team = await create_team(database_with_data, "Team1", game)
    team2: Team = await create_team(database_with_data, "Team2", game)

    player = Player(name="testuser2", password="test")
    database_with_data.add(player)
    await database_with_data.commit()
    
    await add_player(database_with_data, team1, owner)
    await add_player(database_with_data, team2, player)

    await logic_next_round(database_with_data, game, owner)
    topics = [
        "astronomy",
        "telephone",
        "astronomy",
        "royalty",
        "monkeys",
        "pipe organs",
        "pilots",
        "football",
        "volcanoes",
    ]
    for topic in topics:
        card: Card = Card(points=10, topic=topic)
        database_with_data.add(card)
        await database_with_data.commit()
        await logic_add_card_to_game(database_with_data, game, card.card_id)

    await logic_next_round(database_with_data, game, owner)
    assert game.game_started
    
    with pytest.raises(WrongPlayerException):
        await logic_next_round(database_with_data, game, player)


async def test_logic_next_round_your_turn(database_with_data: AsyncSession):
    """Test the logic_next_round function when it's not the player's turn"""
    owner: Player = Player(name="testuser", password="test")
    database_with_data.add(owner)
    await database_with_data.commit()
    new_game = await logic_make_new_game(database_with_data, owner)
    game: Game = await logic_get_game_by_id(new_game.game_id, database_with_data)
    
    
    team1: Team = await create_team(database_with_data, "Team1", game)
    team2: Team = await create_team(database_with_data, "Team2", game)

    player = Player(name="testuser2", password="test")
    database_with_data.add(player)
    await database_with_data.commit()
    
    await add_player(database_with_data, team1, owner)
    await add_player(database_with_data, team2, player)

    await logic_next_round(database_with_data, game, owner)
    topics = [
        "astronomy",
        "telephone",
        "astronomy",
        "royalty",
        "monkeys",
        "pipe organs",
        "pilots",
        "football",
        "volcanoes",
    ]
    for topic in topics:
        card: Card = Card(points=10, topic=topic)
        database_with_data.add(card)
        await database_with_data.commit()
        await logic_add_card_to_game(database_with_data, game, card.card_id)

    await logic_next_round(database_with_data, game, owner)
    assert game.game_started
    
    await logic_next_round(database_with_data, game, owner)
    turn_owner: bool = await logic_get_your_turn(database_with_data, game.game_id, owner)
    turn_player: bool = await logic_get_your_turn(database_with_data, game.game_id, player)

    assert not turn_owner
    assert turn_player



async def test_logic_next_round_game_not_started(database_with_data: AsyncSession):
    """Test the logic_next_round function when the game has not been started"""
    owner: Player = Player(name="testuser", password="test")
    database_with_data.add(owner)
    await database_with_data.commit()
    new_game = await logic_make_new_game(database_with_data, owner)
    game: Game = await logic_get_game_by_id(new_game.game_id, database_with_data)
    
    
    team1: Team = await create_team(database_with_data, "Team1", game)
    team2: Team = await create_team(database_with_data, "Team2", game)

    player = Player(name="testuser2", password="test")
    database_with_data.add(player)
    await database_with_data.commit()
    
    await add_player(database_with_data, team1, owner)
    await add_player(database_with_data, team2, player)

    await logic_next_round(database_with_data, game, owner)
    topics = [
        "astronomy",
        "telephone",
        "astronomy",
        "royalty",
        "monkeys",
        "pipe organs",
        "pilots",
        "football",
        "volcanoes",
    ]
    for topic in topics:
        card: Card = Card(points=10, topic=topic)
        database_with_data.add(card)
        await database_with_data.commit()
        await logic_add_card_to_game(database_with_data, game, card.card_id)
        
    with pytest.raises(WrongPlayerException):
        await logic_next_round(database_with_data, game, player)
