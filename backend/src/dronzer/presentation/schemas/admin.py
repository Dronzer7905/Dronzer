from datetime import datetime

from pydantic import BaseModel


class OrganizationCreate(BaseModel):
    name: str
    billing_email: str | None = None


class OrganizationResponse(BaseModel):
    id: str
    name: str
    billing_email: str | None
    created_at: datetime
    is_active: bool


class ProjectCreate(BaseModel):
    name: str
    org_id: str
    environment: str = "production"


class ProjectResponse(BaseModel):
    id: str
    name: str
    org_id: str
    environment: str
    created_at: datetime


class ProviderConfigResponse(BaseModel):
    id: str
    name: str
    is_enabled: bool
    priority: int
    weight: int
    models: list[str]


from typing import Any


class ModelConfigResponse(BaseModel):
    id: str
    provider_id: str
    name: str
    is_enabled: bool
    context_window: int
    capabilities: dict[str, Any] = {}


class ModelCreate(BaseModel):
    name: str
    provider_id: str
    context_window: int = 8192
