from fastapi import APIRouter, Depends

from dronzer.presentation.api.admin import (
    auth,
    gateway_keys,
    health,
    keys,
    models,
    organizations,
    plugins,
    projects,
    providers,
)
from dronzer.presentation.api.admin.deps import get_current_admin

admin_router = APIRouter(prefix="/admin")

# Auth (Public)
admin_router.include_router(auth.router)

# Protected Admin Routes
protected_router = APIRouter(dependencies=[Depends(get_current_admin)])

# Multi-tenancy
protected_router.include_router(organizations.router)
protected_router.include_router(projects.router)

# Core Management
protected_router.include_router(providers.router)
protected_router.include_router(models.router)
protected_router.include_router(keys.router)
protected_router.include_router(gateway_keys.router)

# System Admin
protected_router.include_router(plugins.router)
protected_router.include_router(health.router)

admin_router.include_router(protected_router)
