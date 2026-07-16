import pytest
from httpx import AsyncClient, ASGITransport
from dronzer.core.main import app
from dronzer.core.exceptions import ConfigurationException


@pytest.mark.asyncio
async def test_health_endpoint():
    """Verify the health endpoint returns 200 OK and expected structure."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "app" in data
        assert "uptime_seconds" in data


@pytest.mark.asyncio
async def test_custom_exception_handler():
    """Verify that DronzerException is caught and formatted properly by the handler."""

    # We dynamically add a throwing route just for testing
    @app.get("/api/v1/test-error")
    async def throw_error():
        raise ConfigurationException("Invalid tenant config", details={"tenant_id": 123})

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        response = await client.get("/api/v1/test-error")
        assert response.status_code == 400
        data = response.json()
        assert data["error"] == "Invalid tenant config"
        assert data["details"]["tenant_id"] == 123
