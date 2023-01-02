"""Logic of games route"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_session
from src.database.crud.game import (get_all_games,
                                    create_game, get_game,
                                    start_suggests_cards,
                                    start_next_round,
                                    next_player)
from src.database.crud.team import get_all_teams_from_game
from src.database.crud.card import reset_cards_game, get_unguessed_cards
from src.database.models import Game, Player, Team, Card


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


async def logic_next_round(database: AsyncSession, game: Game, player: Player) -> None:
    """goed to the next round"""
    current_team: Team = game.teams[game.next_team_index]
    current_player: Player = current_team.players[current_team.next_player_index]
    if current_player != player:
        return
    cards: list[Card] = await get_unguessed_cards(database, game)

    if len(cards) == 0:
        await reset_cards_game(database, game)
        if not game.may_suggests_cards and not game.round_one_done:
            await start_suggests_cards(database, game)
        else:
            await start_next_round(database, game)
    else:
        await next_player(database, game)
