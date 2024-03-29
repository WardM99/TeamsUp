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
from src.database.schemas.game import ReturnGames, ReturnGame
from src.app.exceptions.wrongplayer import WrongPlayerException


async def logic_get_all_games(database: AsyncSession) -> ReturnGames:
    """The logic to get all games"""
    all_games: list[Game] = await get_all_games(database)
    all_return_games: list[ReturnGame] = []
    for game in all_games:
        teams: list[Team] = await get_all_teams_from_game(database, game)
        return_game: ReturnGame = ReturnGame(game_id=game.game_id,
                                round_one_done=game.round_one_done,
                                round_two_done=game.round_two_done,
                                round_three_done=game.round_three_done,
                                may_suggests_cards=game.may_suggests_cards,
                                game_started=game.game_started,
                                owner=game.owner, # type: ignore
                                teams=teams) # type: ignore
        all_return_games.append(return_game)
    return_games: ReturnGames = ReturnGames(games=all_return_games)
    return return_games


async def logic_make_new_game(database: AsyncSession, owner: Player) -> ReturnGame:
    """The logic to create a new game"""
    game: Game = await create_game(database, owner)
    return_game: ReturnGame = ReturnGame(game_id=game.game_id,
                                round_one_done=game.round_one_done,
                                round_two_done=game.round_two_done,
                                round_three_done=game.round_three_done,
                                may_suggests_cards=game.may_suggests_cards,
                                game_started=game.game_started,
                                owner=game.owner, # type: ignore
                                teams=[])
    return return_game


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
    """go to the next round"""
    cards: list[Card] = await get_unguessed_cards(database, game)
    print(cards)
    if len(cards) == 0:
        if player.player_id == game.owner.player_id:
            await reset_cards_game(database, game)
            if not game.may_suggests_cards and not game.game_started:
                await start_suggests_cards(database, game)
            else:
                await start_next_round(database, game)
        else:
            raise WrongPlayerException
    elif not game.game_started and len(cards) > 0 and player.player_id == game.owner.player_id:
        await start_next_round(database, game)
    elif game.game_started and len(cards) > 0:
        myturn: bool = await logic_get_your_turn(database, game.game_id, player)
        if not myturn:
            raise WrongPlayerException
        await next_player(database, game)
    else:
        raise WrongPlayerException
