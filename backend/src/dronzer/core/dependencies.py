from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from dronzer.application.config.manager import ConfigurationManager
from dronzer.domain.ports import ICache, IEventBus
from dronzer.infrastructure.database.core import get_db_session


def get_event_bus(request: Request) -> IEventBus:
    """Provides the EventBus instance."""
    return request.app.state.event_bus


def get_cache(request: Request) -> ICache:
    """Provides the Cache instance."""
    return request.app.state.cache


def get_config_manager(
    cache: ICache = Depends(get_cache), event_bus: IEventBus = Depends(get_event_bus)
) -> ConfigurationManager:
    """Provides the Configuration Manager for dynamic settings."""
    return ConfigurationManager(cache=cache, event_bus=event_bus)


def get_db(session: AsyncSession = Depends(get_db_session)) -> AsyncSession:
    """Alias for getting DB session."""
    return session
