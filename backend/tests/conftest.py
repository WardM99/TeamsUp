"""Pytest configuration file with fixtures"""
from typing import AsyncGenerator
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from alembic import config, command
from src.database.database import engine



@pytest.fixture(scope="session")
def tables():
    """
    Fixture to initialize a database before the tests,
    and drop it again afterwards
    """
    alembic_config: config.Config = config.Config('alembic.ini')
    command.upgrade(alembic_config, 'head')
    yield
    command.downgrade(alembic_config, 'base')

@pytest.fixture
async def database_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Fixture to create a session for every test, and rollback
    all the transactions so that each tests starts with a clean db
    """
    connection = await engine.connect()
    transaction = await connection.begin()
    # AsyncSession needs expire_on_commit to be False
    session = AsyncSession(bind=connection, expire_on_commit=False)
    yield session

    # Clean up connections & rollback transactions
    await session.close()

    # Transactions can be invalidated when an exception is raised
    # which causes warnings when running the tests
    # Check if a transaction is still valid before rolling back
    if transaction.is_valid:
        await transaction.rollback()

    await connection.close()
