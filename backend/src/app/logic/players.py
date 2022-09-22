"""Logic of players route"""
from datetime import timedelta, datetime
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.crud.player import get_player, get_players_team, create_player
from src.database.schemas.player import Token
from src.database.models import Team, Player

async def logic_get_all_players(database: AsyncSession, team: Team) -> list[Player]:
    """The logic to get all players of a team"""
    return await get_players_team(database, team)


async def logic_make_new_player(database: AsyncSession, team: Team, name: str) -> Player:
    """The logic to create a new player"""
    return await create_player(database, name, team)


async def logic_get_player_by_id(database: AsyncSession, team: Team, player_id: int) -> Player:
    """The logic to get a player by id"""
    return await get_player(database, player_id, team)


async def logic_generate_token(player: Player) -> Token:
    """The logic to create a token"""
    access_token = create_token(player)
    return Token(
        access_token=access_token,
        token_type="bearer",
        player=player
    )


def create_token(player: Player):
    """Create an access token"""
    data: dict = {"type": "access", "sub": str(player.player_id)}
    data["exp"] = datetime.utcnow() + timedelta(hours=2)
    return jwt.encode(
        data,
        "WPll6MnvmR1NLf7x6jszNNXlQUwhqpKIyIUyQdg3zio7ngodp82FRbh1JM4UO5qZ",
        algorithm="HS256"
    )
