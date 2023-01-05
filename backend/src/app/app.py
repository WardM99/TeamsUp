"""Startup of FastAPI application"""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from environs import Env
from alembic import config, script
from alembic.runtime import migration

from src.app.exceptions.handler import install_handlers
from src.database.database import engine
from src.database.exceptions import PendingMigrationsException
from src.app.routers.players.players import players_router
from .routers import games_router


app = FastAPI(
    title="TeamsUp",
    version="0.0.1"
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


@app.on_event('startup')
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
async def root():
    """give a Hello World message"""
    return {"message": "Hello World"}
