"""Schemas for a game"""
from src.database.schemas.utils import OrmModel
from src.database.schemas.team import ReturnTeam


class ReturnGame(OrmModel):
    """Represents a game"""
    game_id: int
    round_one_done: bool
    round_two_done: bool
    round_three_done: bool
    teams: list[ReturnTeam]
