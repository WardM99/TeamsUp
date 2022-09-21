"""Logic of players route"""
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.crud.player import get_player, get_players_team, create_player
from src.database.models import Team, Player

async def logic_get_all_players(database: AsyncSession, team: Team) -> list[Player]:
    """The logic to get all players of a team"""
    return await get_players_team(database, team)


async def logic_make_new_player(database: AsyncSession, team: Team, name: str) -> Player:
    """The logic to create a new player"""
    return await create_player(database, name, team)


async def logic_get_player_by_id(database: AsyncSession, team: Team, player_id: int) -> Player:
    """The logic to get a player by id"""
    return await get_player(database, player_id, team)
