"""Games routers"""
from fastapi import APIRouter

games_router = APIRouter(prefix=("/games"))

@games_router.get("")
def get_game():
    """Get all games"""
    return {"test": "test"}
