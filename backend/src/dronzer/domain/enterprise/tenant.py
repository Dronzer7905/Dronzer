from typing import Any

import structlog
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

logger = structlog.get_logger("dronzer.enterprise.tenant")


class TenantContext(BaseModel):
    """
    Identifies the active tenant (Organization & Project) for the current request flow.
    Used by the Gateway routing engine to enforce isolation and apply quotas.
    """

    organization_id: str
    project_id: str
    organization_slug: str
    is_active: bool
    settings: dict[str, Any] = {}


class TenantIsolationException(Exception):
    pass


class TenantService:
    """
    Core Domain Service for Multi-Tenant lifecycle management.
    """

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_tenant_context_by_api_key(self, api_key_hash: str) -> TenantContext | None:
        """
        Resolves a Vaulted API Key to its owning Project and Organization.
        This allows the Gateway to establish a TenantContext for routing.
        """
        # Pseudo-code for DB retrieval:
        # result = await self.db.execute(
        #     select(Project, Organization)
        #     .join(Organization)
        #     .join(APIKey)
        #     .where(APIKey.key_hash == api_key_hash)
        # )
        # data = result.first()
        # if not data: return None
        # return TenantContext( organization_id=data.Organization.id, ... )
        pass

    def enforce_isolation(self, active_tenant: TenantContext, requested_resource_org_id: str):
        """
        Hard-enforces logical tenant boundaries.
        Should be called before any DB write or sensitive read.
        """
        if active_tenant.organization_id != requested_resource_org_id:
            logger.critical(
                "TENANT ISOLATION BREACH DETECTED",
                active_tenant=active_tenant.organization_id,
                target_tenant=requested_resource_org_id,
            )
            raise TenantIsolationException("Cross-tenant resource access is strictly forbidden.")
