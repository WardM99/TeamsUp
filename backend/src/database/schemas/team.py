"""Schemas for a team"""
from src.database.schemas.utils import OrmModel, BaseModel
from src.database.schemas.player import ReturnPlayer


class ReturnTeam(OrmModel):
    """Represents a team"""
    team_id: int
    game_id: int
    team_name: str
    players: list[ReturnPlayer]


class ReturnTeams(OrmModel):
    """Represents a list of teams"""
    teams: list[ReturnTeam]

class InputTeam(BaseModel):
    """Input details of a team"""
    team_name: str
