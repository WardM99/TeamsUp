from datetime import timedelta
from typing import Text

from requests import Response
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from src.app.logic.players import create_token
from src.database.models import Player


class AuthClient(AsyncClient):
    """Custom TestClient that handles authentication to make tests more compact"""
    user: Player | None = None
    headers: dict[str, str] | None = None
    session: AsyncSession

    def __init__(self, session: AsyncSession, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session = session

    def invalid(self):
        """Sign in with an invalid access token"""
        self.headers = {
            "Authorization": "Bearer If I can't scuba, then what has this all been about? What am I working towards?"
        }

    async def player(self):
        """Sign in as an admin for all future requests"""
        # Create a new user in the db
        player = Player(name="Player1", password="Wachtwoord")
        self.session.add(player)
        await self.session.commit()

        self.login(player)

    def login(self, user: Player):
        """Sign in as a user for all future requests"""
        self.user = user

        # Since an authclient is created for every test, the access_token will most likely not run out
        access_token = create_token(user)

        # Add auth headers into dict
        self.headers = {"Authorization": f"Bearer {access_token}"}

    async def delete(self, url: Text | None, **kwargs) -> Response:
        if self.headers is not None:
            kwargs["headers"] = self.headers

        return await super().delete(url, **kwargs)

    async def get(self, url: Text | None, **kwargs) -> Response:
        if self.headers is not None:
            kwargs["headers"] = self.headers

        return await super().get(url, **kwargs)

    async def patch(self, url: Text | None, **kwargs) -> Response:
        if self.headers is not None:
            kwargs["headers"] = self.headers

        return await super().patch(url, **kwargs)

    async def post(self, url: Text | None, **kwargs) -> Response:
        if self.headers is not None:
            kwargs["headers"] = self.headers

        return await super().post(url, **kwargs)

    async def put(self, url: Text | None, **kwargs) -> Response:
        if self.headers is not None:
            kwargs["headers"] = self.headers

        return await super().put(url, **kwargs)
