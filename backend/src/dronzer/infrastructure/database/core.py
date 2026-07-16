from collections.abc import AsyncGenerator

import structlog
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import AsyncAdaptedQueuePool

from dronzer.core.config import settings

logger = structlog.get_logger("dronzer.database")


def get_engine() -> AsyncEngine:
    """
    Creates the SQLAlchemy AsyncEngine with connection pooling tuned for high throughput.
    """
    return create_async_engine(
        settings.DATABASE_URL,
        poolclass=AsyncAdaptedQueuePool,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_pre_ping=True,  # Health check before handing out connections
        echo=settings.DEBUG,  # Log SQL in debug mode
    )


engine = get_engine()

# Global async session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    """
    FastAPI dependency that yields a database session.
    Automatically handles rollback on exceptions and closes the session.
    """
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Test the database connection during startup.
    (Table creation is handled by Alembic, not here).
    """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: None)
        logger.info("Database connection established successfully.")
    except Exception as e:
        logger.exception("Failed to connect to the database.", exc_info=e)
        raise
