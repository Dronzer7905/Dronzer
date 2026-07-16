from fastapi.testclient import TestClient

from dronzer.presentation.api.server import create_app

# Create a test instance of the app
app = create_app()
client = TestClient(app)


def test_liveness_probe():
    response = client.get("/health/liveness")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readiness_probe():
    response = client.get("/health/readiness")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_auth_middleware_blocks_unauthorized():
    # Attempting to access a protected v1 route without an API key
    response = client.get("/v1/models")
    assert response.status_code == 401
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "missing_api_key"


from unittest.mock import AsyncMock, MagicMock, patch


@patch("dronzer.presentation.api.middleware.auth.async_session_factory")
def test_auth_middleware_allows_authorized(mock_factory):
    # Pass a bearer token (even a fake one) to test the middleware allows it through
    # We mock the state for the test
    from dronzer.application.registry.provider import ProviderRegistry

    app.state.provider_registry = ProviderRegistry()

    # Mock the DB session and result
    mock_session = AsyncMock()
    mock_factory.return_value.__aenter__.return_value = mock_session
    mock_result = MagicMock()
    mock_db_key = MagicMock()
    mock_db_key.id = "mock-id"
    mock_db_key.organization_id = "org-id"
    mock_db_key.project_id = "proj-id"
    mock_db_key.task_type = "general"
    mock_db_key.model_priorities = []
    mock_db_key.provider_priorities = []
    mock_result.scalars().first.return_value = mock_db_key
    mock_session.execute.return_value = mock_result

    response = client.get("/v1/models", headers={"Authorization": "Bearer test-key"})
    assert response.status_code == 200
    data = response.json()
    assert data["object"] == "list"
    assert isinstance(data["data"], list)


@patch("dronzer.presentation.api.middleware.auth.async_session_factory")
def test_validation_error_format(mock_factory):
    # Pass bad data to an endpoint to verify OpenAI-compatible 400 responses
    # We mock the pipeline state
    class MockPipeline:
        pass

    app.state.pipeline = MockPipeline()

    # Mock the DB session and result
    mock_session = AsyncMock()
    mock_factory.return_value.__aenter__.return_value = mock_session
    mock_result = MagicMock()
    mock_db_key = MagicMock()
    mock_db_key.id = "mock-id"
    mock_db_key.organization_id = "org-id"
    mock_db_key.project_id = "proj-id"
    mock_db_key.task_type = "general"
    mock_db_key.model_priorities = []
    mock_db_key.provider_priorities = []
    mock_result.scalars().first.return_value = mock_db_key
    mock_session.execute.return_value = mock_result

    response = client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer test"},
        json={"model": "test"},  # Missing 'messages' field
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["type"] == "invalid_request_error"
    assert "messages" in data["error"]["param"]
