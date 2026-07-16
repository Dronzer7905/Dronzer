import pytest


@pytest.fixture
def mock_app():
    return {"status": "ok"}
