"""Logic of players route"""
from datetime import timedelta, datetime
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.crud.player import create_player, get_player_by_id
from src.database.schemas.player import Token
from src.database.database import get_session
from src.database.models import Team, Player

#async def logic_get_all_players(database: AsyncSession, team: Team) -> list[Player]:
#    """The logic to get all players of a team"""
#    return await get_players_team(database, team)
#
#
#async def logic_make_new_player(database: AsyncSession, team: Team, name: str) -> Player:
#    """The logic to create a new player"""
#    return await create_player(database, name, team)
#
#
#async def logic_get_player_by_id(database: AsyncSession, team: Team, player_id: int) -> Player:
#    """The logic to get a player by id"""
#    return await get_player(database, player_id, team)


async def logic_generate_token(player: Player) -> Token:
    """The logic to create a token"""
    access_token = create_token(player)
    return Token(
        access_token=access_token,
        token_type="bearer",
        player=player
    )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="")


def create_token(player: Player):
    """Create an access token"""
    data: dict = {"type": "access", "sub": str(player.player_id)}
    data["exp"] = datetime.utcnow() + timedelta(hours=2)
    return jwt.encode(
        data,
        "WPll6MnvmR1NLf7x6jszNNXlQUwhqpKIyIUyQdg3zio7ngodp82FRbh1JM4UO5qZ",
        algorithm="HS256"
    )


async def get_user_from_access_token(
    database: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme)
) -> Player:
    """Test"""
    payload = jwt.decode(
        token,
        "WPll6MnvmR1NLf7x6jszNNXlQUwhqpKIyIUyQdg3zio7ngodp82FRbh1JM4UO5qZ",
        algorithms="HS256"
    )
    user_id: int | None = payload.get("sub")
    type_in_token: int | None = payload.get("type")

    if user_id is None or type_in_token is None:
        raise JWTError()

    player = await get_player_by_id(database, int(user_id))
    return player


async def require_player(player: Player = Depends(get_user_from_access_token)) -> Player:
    """Test"""
    return player
