"""Test logic players"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.logic.players import logic_make_new_player, logic_get_player_by_name_and_password
from src.database.models import Player

async def test_get_player_by_name_and_password(database_session: AsyncSession):
    """Test the logic of get player by name and password"""
    player_new: Player = await logic_make_new_player(database_session, "Joske", "PW1")
    assert player_new.name == "Joske"
    player: Player = await logic_get_player_by_name_and_password(database_session, "Joske", "PW1")
    assert player == player_new
