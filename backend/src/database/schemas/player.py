"""Schemas for a player"""
from src.database.schemas.utils import OrmModel, BaseModel


class ReturnPlayer(OrmModel):
    """Represents a player"""
    player_id: int
    name: str


class Token(BaseModel):
    """Token generated after a player is created"""
    access_token: str
    token_type: str
    player: ReturnPlayer


class ReturnPlayers(OrmModel):
    """Represents a list of players"""
    players: list[ReturnPlayer]


class InputPlayer(BaseModel):
    """Input details of a player"""
    name: str
    password: str
