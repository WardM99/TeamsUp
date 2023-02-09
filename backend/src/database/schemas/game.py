"""Schemas for a game"""
from src.database.schemas.utils import OrmModel
from src.database.schemas.player import ReturnPlayer
from src.database.schemas.team import ReturnTeam

class ReturnGame(OrmModel):
    """Represents a game"""
    game_id: int
    round_one_done: bool
    round_two_done: bool
    round_three_done: bool
    may_suggests_cards: bool
    game_started: bool
    owner: ReturnPlayer
    teams: list[ReturnTeam]

class ReturnGameStatus(OrmModel):
    """Represents the game statuses"""
    game_id: int
    round_one_done: bool
    round_two_done: bool
    round_three_done: bool
    may_suggests_cards: bool
    owner: ReturnPlayer


class ReturnGames(OrmModel):
    """Represents a list of games"""
    games: list[ReturnGame]


class ReturnTurn(OrmModel):
    """Represents if it's your turn or not"""
    your_turn: bool
