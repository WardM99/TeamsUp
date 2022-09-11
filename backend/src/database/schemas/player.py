"""Schemas for a player"""
from src.database.schemas.utils import OrmModel, BaseModel


class ReturnPlayer(OrmModel):
    """Represents a player"""
    player_id: int
    team_id: int
    name: str


class InputPlayer(BaseModel):
    """Input details of a player"""
    team_id: int
    name: str
