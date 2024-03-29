"""Logic of players route"""
from datetime import timedelta, datetime
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from src.app.exceptions.wrongcredentials import WrongCredentialsException
from src.database.crud.player import (create_player,
                                      get_player_by_id,
                                      get_player_by_name)
from src.database.schemas.player import Token
from src.database.database import get_session
from src.database.models import Player

# Configuration

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def logic_make_new_player(database: AsyncSession, name: str, password: str) -> Player:
    """The logic to create a new player"""
    return await create_player(database, name, pwd_context.hash(password))


async def logic_get_player_by_id(database: AsyncSession, player_id: int) -> Player:
    """The logic to get a player by id"""
    return await get_player_by_id(database, player_id)


async def logic_generate_token(player: Player) -> Token:
    """The logic to create a token"""
    access_token = create_token(player)
    return Token(
        access_token=access_token,
        token_type="bearer",
        player=player # type: ignore
    )


async def logic_get_player_by_name_and_password(database: AsyncSession,
                                                name: str,
                                                password: str) -> Player:
    """The logic to get a player by name and password"""
    try:
        player: Player = await get_player_by_name(database, name)
        if verify_password(password, player.password):
            return player
        raise WrongCredentialsException
    except NoResultFound as exc:
        raise WrongCredentialsException from exc


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/players/login")


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
    """Get the user from an access token"""
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
    """Require a player to be logged in"""
    return player


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that a password matches a hash found in the database"""
    return pwd_context.verify(plain_password, hashed_password)
