"""Schemas for a card"""
from src.database.schemas.utils import OrmModel, BaseModel


class ReturnCard(OrmModel):
    """Represents a card"""
    card_id: int
    points: int
    topic: str


class ReturnCardList(OrmModel):
    """Represents a list of cards"""
    cards: list[ReturnCard]

class InputCard(BaseModel):
    """Input of a card"""
    card_id: int
