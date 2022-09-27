"""Logic of games route"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_session
from src.database.crud.game import get_all_games, create_game, get_game
from src.database.crud.team import get_all_teams_from_game
from src.database.models import Game, Player, Team


async def logic_get_all_games(database: AsyncSession) -> list[Game]:
    """The logic to get all games"""
    return await get_all_games(database)


async def logic_make_new_game(database: AsyncSession, owner: Player) -> Game:
    """The logic to create a new game"""
    return await create_game(database, owner)


async def logic_get_game_by_id(game_id: int, database: AsyncSession = Depends(get_session)) -> Game:
    """The logic to get a game by id"""
    return await get_game(database, game_id)


async def logic_get_your_turn(database: AsyncSession, game_id: int|None, player: Player) -> bool:
    """The logic to know if it's your turn or not"""
    if game_id is not None:
        game: Game = await get_game(database, game_id)
        teams: list[Team] = await get_all_teams_from_game(database, game)
        team_turn: Team = teams[game.next_team_index]
        return team_turn.players[team_turn.next_player_index] == player
    return False
