"""Schemas for a game"""
from src.database.schemas.utils import OrmModel
from src.database.schemas.player import ReturnPlayer


class ReturnGame(OrmModel):
    """Represents a game"""
    game_id: int
    round_one_done: bool
    round_two_done: bool
    round_three_done: bool
    owner: ReturnPlayer


class ReturnGames(OrmModel):
    """Represents a list of games"""
    games: list[ReturnGame]


class ReturnTurn(OrmModel):
    """Represents if it's your turn or not"""
    your_turn: bool
