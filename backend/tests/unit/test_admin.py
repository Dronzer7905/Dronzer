from fastapi.testclient import TestClient

from dronzer.domain.admin.rbac import Permission, Role, has_permission
from dronzer.presentation.api.admin.deps import get_current_admin
from dronzer.presentation.api.admin.router import admin_router
from dronzer.presentation.api.server import create_app

# Attach the admin router for the test
app = create_app()
app.include_router(admin_router)

# Override admin auth dependency
app.dependency_overrides[get_current_admin] = lambda: {
    "sub": "test@admin.com",
    "role": "SUPER_ADMIN",
    "type": "access",
}

client = TestClient(app)


def test_rbac_logic():
    # Super Admin can do everything
    assert has_permission(Role.SUPER_ADMIN, Permission.MANAGE_SYSTEM)
    assert has_permission(Role.SUPER_ADMIN, Permission.MANAGE_PROJECT)

    # Read-Only developer
    assert has_permission(Role.READ_ONLY, Permission.VIEW_METRICS)
    assert not has_permission(Role.READ_ONLY, Permission.MANAGE_PROJECT)


def test_admin_orgs_list():
    response = client.get("/admin/organizations")
    # In auth testing, we mock the auth headers if the middleware blocks it.
    # Our middleware only blocks /v1 routes currently, so this should pass through.
    assert response.status_code == 200
    assert isinstance(response.json(), list)


from unittest.mock import AsyncMock, patch


@patch("dronzer.infrastructure.database.core.async_session_factory")
def test_admin_providers_list(mock_factory):
    from dronzer.application.registry.provider import ProviderRegistry

    # Mock the DB session
    mock_session = AsyncMock()
    mock_factory.return_value.__aenter__.return_value = mock_session
    mock_session.execute.return_value.scalars.return_value.all.return_value = []

    app.state.provider_registry = ProviderRegistry()
    response = client.get("/admin/providers")
    assert response.status_code == 200
