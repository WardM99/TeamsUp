"""Startup of FastAPI application"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from starlette.middleware.cors import CORSMiddleware
from environs import Env
from alembic import config, script
from alembic.runtime import migration

from src.app.exceptions.handler import install_handlers
from src.database.database import engine, get_session
from src.database.exceptions import PendingMigrationsException
from src.app.routers.players.players import players_router
from src.app.logic.cards import logic_add_cards_to_database, logic_get_cards
from src.app.logic.players import require_player
from src.database.schemas.card import ReturnCardList
from .routers import games_router

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """lifespan"""
    print("lifespan start")
    init_database()
    yield
    # Clean up the ML models and release the resources
    print("lifespan end")

app = FastAPI(
    title="TeamsUp",
    version="0.0.1",
    lifespan=lifespan
)
env = Env()

# Read the .env file
env.read_env()
CORS_ORIGINS: list[str] = env.list("CORS_ORIGINS", ["http://localhost:3000"])

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
install_handlers(app)


# Include routes
app.include_router(games_router)
app.include_router(players_router)


async def init_database(): # pragma: no cover
    """Create all tables of database"""
    alembic_config: config.Config = config.Config('alembic.ini')
    alembic_script: script.ScriptDirectory = script.ScriptDirectory.from_config(alembic_config)
    async with engine.begin() as conn:
        revision: str = await conn.run_sync(
            lambda sync_conn: migration.MigrationContext.configure(sync_conn).get_current_revision()
        )
        alembic_head: str = alembic_script.get_current_head()
        if revision != alembic_head:
            raise PendingMigrationsException


@app.get("/",)
async def root(): # pragma: no cover
    """give a Hello World message"""
    return {"message": "Hello World"}

@app.post("/cards", status_code=status.HTTP_201_CREATED
          ,dependencies=[Depends(require_player)])
async def add_cards(database: AsyncSession = Depends(get_session)): # pragma: no cover
    """add cards"""
    await logic_add_cards_to_database(database)


@app.get("/cards", status_code=status.HTTP_200_OK, response_model=ReturnCardList
         ,dependencies=[Depends(require_player)])
async def get_cards(database: AsyncSession = Depends(get_session)): # pragma: no cover
    """return cards"""
    card_list = ReturnCardList(cards=await logic_get_cards(database)) # type: ignore
    return card_list
