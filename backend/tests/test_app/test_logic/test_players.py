"""Test logic players"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.logic.players import logic_make_new_player, logic_get_player_by_name_and_password
from src.app.exceptions.wrongcredentials import WrongCredentialsException
from src.database.models import Player

async def test_get_player_by_name_and_password(database_session: AsyncSession):
    """Test the logic of get player by name and password"""
    player_new: Player = await logic_make_new_player(database_session, "Joske", "PW1")
    assert player_new.name == "Joske"
    player: Player = await logic_get_player_by_name_and_password(database_session, "Joske", "PW1")
    assert player == player_new


async def test_get_player_by_name_and_wrong_password(database_session: AsyncSession):
    """Test the logic of get player by name and wrong password"""
    player_new: Player = await logic_make_new_player(database_session, "Joske", "PW1")
    assert player_new.name == "Joske"
    with pytest.raises(WrongCredentialsException):
        await logic_get_player_by_name_and_password(database_session, "Joske", "PW2")


async def test_get_player_by_wrong_name_and_password(database_session: AsyncSession):
    """Test the logic of get player by name and wrong password"""
    player_new: Player = await logic_make_new_player(database_session, "Joske", "PW1")
    assert player_new.name == "Joske"
    with pytest.raises(WrongCredentialsException):
        await logic_get_player_by_name_and_password(database_session, "joske", "PW1")
