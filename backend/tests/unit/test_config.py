import pytest
from unittest.mock import AsyncMock

from dronzer.application.config.manager import ConfigurationManager


@pytest.mark.asyncio
async def test_configuration_manager_cache_miss():
    """Verify Configuration Manager loads from DB on cache miss."""
    mock_cache = AsyncMock()
    mock_cache.get.return_value = None

    manager = ConfigurationManager(cache=mock_cache)

    # We mock fetch from DB for unit test isolation
    manager._fetch_from_db = AsyncMock(return_value={"MAX_TOKENS": 1000})

    config = await manager.load()

    assert config["MAX_TOKENS"] == 1000
    mock_cache.set.assert_called_once()
    assert manager.get("MAX_TOKENS") == 1000
