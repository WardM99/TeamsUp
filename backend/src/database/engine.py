"""Engine of the database"""
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine: AsyncEngine

# Use sqlite database.
engine = create_async_engine(URL.create(
    drivername="sqlite+aiosqlite",
    database="test.db"
), connect_args={"check_same_thread": False})

# AsyncSession needs expire_on_commit to be False
DBSession = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False
)
