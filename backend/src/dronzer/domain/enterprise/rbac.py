from typing import Any

import structlog
from pydantic import BaseModel

logger = structlog.get_logger("dronzer.enterprise.rbac")


class ResourceContext(BaseModel):
    """
    Context about the resource being accessed for Attribute-Based Access Control (ABAC).
    """

    resource_type: str  # e.g., 'project', 'api_key', 'model'
    resource_id: str
    organization_id: str
    project_id: str | None = None
    attributes: dict[str, Any] = {}  # e.g., {'is_production': True, 'cost_tier': 'premium'}


class UserContext(BaseModel):
    """
    Context about the User requesting access.
    """

    user_id: str
    organization_id: str
    roles: list[str]  # List of role names or IDs
    permissions: list[str]  # Flattened list of all explicit permissions granted to this user
    attributes: dict[str, Any] = {}  # e.g., {'department': 'engineering', 'clearance': 'high'}


class PolicyEngine:
    """
    Evaluates dynamic, hierarchical access control policies.
    Supports both traditional RBAC (Roles/Permissions) and ABAC (Context matching).
    """

    def _evaluate_rbac(self, required_permission: str, user: UserContext) -> bool:
        """
        Check if the user has the explicit permission.
        Supports wildcard matching (e.g., 'projects:*' matches 'projects:read').
        """
        if required_permission in user.permissions:
            return True

        # Wildcard evaluation
        for p in user.permissions:
            if p.endswith(":*"):
                domain = p.split(":")[0]
                if required_permission.startswith(f"{domain}:"):
                    return True

        return False

    def _evaluate_abac(self, action: str, user: UserContext, resource: ResourceContext) -> bool:
        """
        Evaluate context-aware rules.
        Example: "User cannot edit Production Project API Keys unless they are in Engineering."
        """
        # Strict Tenant Isolation Rule: A user can never access resources outside their organization
        if user.organization_id != resource.organization_id:
            logger.warning(
                "ABAC Block: Cross-tenant access attempt",
                user_id=user.user_id,
                target_org=resource.organization_id,
            )
            return False

        # Example dynamic policy checking
        if resource.resource_type == "api_key" and action == "delete":
            if resource.attributes.get("is_production") is True:
                if user.attributes.get("department") != "engineering":
                    logger.warning(
                        "ABAC Block: Non-engineer attempting to delete prod key",
                        user_id=user.user_id,
                    )
                    return False

        return True

    def check_access(self, action: str, resource: ResourceContext, user: UserContext) -> bool:
        """
        Main entrypoint for access evaluation.
        Access is granted ONLY if BOTH RBAC and ABAC engines approve.
        """
        # 1. RBAC Check (Does the user hold the capability?)
        required_permission = f"{resource.resource_type}:{action}"
        has_rbac = self._evaluate_rbac(required_permission, user)

        if not has_rbac:
            logger.debug(f"RBAC Deny: User lacks {required_permission}", user_id=user.user_id)
            return False

        # 2. ABAC Check (Does the context allow the capability?)
        has_abac = self._evaluate_abac(action, user, resource)

        if not has_abac:
            logger.debug("ABAC Deny: Context rules failed", user_id=user.user_id)
            return False

        return True
