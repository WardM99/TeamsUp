"""Teams routers"""
from fastapi import APIRouter

teams_router = APIRouter(prefix="/teams")

@teams_router.get("")
async def get_teams():
    """Get all teams of a game"""
    return {"detail": "Not Implemented"}


@teams_router.post("")
async def make_team():
    """Make new team for this game"""
    return {"detail": "Not Implemented"}


@teams_router.get("/{team_id}")
async def get_team_by_id():
    """Get a team by id"""
    return {"detail": "Not Implemented"}
