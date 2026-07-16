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


from unittest.mock import AsyncMock, MagicMock


def test_admin_providers_list():
    from dronzer.application.registry.provider import ProviderRegistry
    from dronzer.infrastructure.database.core import get_db_session

    # Create a mock async session where execute() is async but
    # the Result object it returns uses synchronous scalars()/all()
    mock_session = AsyncMock(spec_set=["execute", "close", "rollback"])
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_session.execute.return_value = mock_result

    async def override_get_db_session():
        yield mock_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    try:
        app.state.provider_registry = ProviderRegistry()
        response = client.get("/admin/providers")
        assert response.status_code == 200
    finally:
        app.dependency_overrides.pop(get_db_session, None)
