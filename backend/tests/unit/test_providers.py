import pytest
from dronzer.infrastructure.providers.mock import MockProvider


@pytest.mark.asyncio
async def test_mock_provider_health():
    """Verify the mock provider always returns true for health checks."""
    provider = MockProvider()
    assert await provider.check_health("fake-key") is True


@pytest.mark.asyncio
async def test_mock_provider_capabilities():
    """Verify capabilities reflect the setup correctly."""
    provider = MockProvider()
    caps = await provider.get_capabilities()
    assert caps.chat is True
    assert caps.vision is True
    assert caps.tool_calling is True


@pytest.mark.asyncio
async def test_mock_provider_generate():
    """Verify mock provider generates standard responses."""
    provider = MockProvider()
    response = await provider.generate_chat({"model": "test"}, "fake-key")
    assert response["choices"][0]["message"]["content"] == "This is a mocked response for testing."
