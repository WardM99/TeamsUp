"""Schemas for a card"""
from src.database.schemas.utils import OrmModel, BaseModel


class ReturnCard(OrmModel):
    """Represents a card"""
    card_id: int
    points: int
    topic: str


class InputCard(BaseModel):
    """Input of a card"""
    card_id: int
