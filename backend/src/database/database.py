"""Code to make a database connection"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///database.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo = True
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:  # pragma: no cover
    """FastAPI dependency to inject a database session into a route instead of using an import
    Allows the tests to replace it with another database session (not hard coding the session)
    """

    session = SessionLocal()

    # Use "yield" and "finally" to close the session when it's no longer needed
    try:
        yield session
    finally:
        await session.close()
