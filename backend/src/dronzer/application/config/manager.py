from typing import Any

import structlog
from sqlalchemy import select

from dronzer.domain.ports import ICache, IEventBus
from dronzer.infrastructure.database.core import async_session_factory
from dronzer.infrastructure.database.models.system import SystemSetting

logger = structlog.get_logger("dronzer.config")


class ConfigurationManager:
    """
    Manages fetching and hot-reloading dynamic configuration from the DB.
    Combines BaseSettings (env) with dynamic overrides (DB).
    """
    CACHE_KEY = "dronzer:config:system_settings"

    def __init__(self, cache: ICache, event_bus: IEventBus | None = None) -> None:
        self.cache = cache
        self.event_bus = event_bus
        self._local_cache: dict[str, Any] = {}

    async def _fetch_from_db(self) -> dict[str, Any]:
        """Fetches all system settings from the PostgreSQL DB."""
        async with async_session_factory() as session:
            stmt = select(SystemSetting)
            result = await session.execute(stmt)
            settings = result.scalars().all()
            return {s.key: s.value for s in settings}

    async def load(self, force_refresh: bool = False) -> dict[str, Any]:
        """Loads config, utilizing Redis cache heavily."""
        if not force_refresh:
            cached = await self.cache.get(self.CACHE_KEY)
            if cached:
                self._local_cache = cached
                return self._local_cache

        logger.info("Cache miss or force refresh. Loading config from DB.")
        db_config = await self._fetch_from_db()
        await self.cache.set(self.CACHE_KEY, db_config, ttl=3600)
        self._local_cache = db_config
        return self._local_cache

    async def reload(self) -> None:
        """Triggered via pub-sub to atomically reload the config memory state."""
        logger.info("Hot reload triggered for configuration.")
        await self.load(force_refresh=True)

    def get(self, key: str, default: Any = None) -> Any:
        """O(1) memory lookup for configuration variables."""
        return self._local_cache.get(key, default)
