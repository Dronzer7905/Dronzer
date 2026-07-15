import pytest
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

def test_auth_middleware_allows_authorized():
    # Pass a bearer token (even a fake one) to test the middleware allows it through
    # Note: Without a mocked registry, this might return 500 if the state isn't populated,
    # but the auth layer itself should pass.
    
    # We mock the state for the test
    from dronzer.application.registry.provider import ProviderRegistry
    app.state.provider_registry = ProviderRegistry()
    
    response = client.get("/v1/models", headers={"Authorization": "Bearer test-key"})
    assert response.status_code == 200
    data = response.json()
    assert data["object"] == "list"
    assert isinstance(data["data"], list)

def test_validation_error_format():
    # Pass bad data to an endpoint to verify OpenAI-compatible 400 responses
    # We mock the pipeline state
    class MockPipeline:
        pass
    app.state.pipeline = MockPipeline()
    
    response = client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer test"},
        json={"model": "test"} # Missing 'messages' field
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["type"] == "invalid_request_error"
    assert "messages" in data["error"]["param"]
