"""Cards routers"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.database import get_session
from src.app.logic.players import require_player
from src.database.models import Game, Player, Card

card_router = APIRouter(prefix="/cards")

@card_router.get("", dependencies=[Depends(require_player)])
async def get_next_card(database: AsyncSession = Depends(get_session)):
    """Get next card"""
    return {"details": "Not Implemented"}


@card_router.post("", dependencies=[Depends(require_player)])
async def add_card(database: AsyncSession = Depends(get_session)):
    """Add a card to game"""
    return {"details": "Not Implemented"}


@card_router.post("/{card_id}", dependencies=[Depends(require_player)])
async def correct_card(database: AsyncSession = Depends(get_session)):
    """Card is guessed correctly"""
    return {"details": "Not Implemented"}


@card_router.patch("/{card_id}")
async def overrule_previous_card(database: AsyncSession = Depends(get_session), owner: Player = Depends(require_player)):
    """Overrule the previous card when selected wrongly"""
    return {"details": "Not Implemented"}
