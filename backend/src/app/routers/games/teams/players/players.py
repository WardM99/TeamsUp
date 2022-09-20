"""Players routers"""
from fastapi import APIRouter, Depends

players_router = APIRouter(prefix="/players")

@players_router.get("")
async def get_players():
    """Get all players of a team"""
    return {"detail": "Not Implemented"}


@players_router.post("")
async def make_player():
    """Make a new player for this team"""
    return {"detail": "Not Implemented"}


@players_router.get("/{player_id}")
async def get_player_by_id():
    """Get a player by id"""
    return {"detail": "Not Implemented"}
    