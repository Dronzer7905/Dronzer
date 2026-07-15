from enum import Enum


class Permission(str, Enum):
    # Global Admin
    MANAGE_SYSTEM = "system:manage"
    VIEW_SYSTEM = "system:view"

    # Organization
    MANAGE_ORG = "org:manage"
    VIEW_ORG = "org:view"
    MANAGE_ORG_MEMBERS = "org:members:manage"

    # Project
    MANAGE_PROJECT = "project:manage"
    VIEW_PROJECT = "project:view"

    # Providers & Models
    MANAGE_PROVIDERS = "providers:manage"
    VIEW_PROVIDERS = "providers:view"

    # Keys & Routing
    MANAGE_KEYS = "keys:manage"
    VIEW_KEYS = "keys:view"
    MANAGE_ROUTING = "routing:manage"

    # Observability
    VIEW_METRICS = "metrics:view"
    VIEW_AUDIT = "audit:view"

class Role(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ORG_OWNER = "ORG_OWNER"
    ORG_ADMIN = "ORG_ADMIN"
    PROJECT_ADMIN = "PROJECT_ADMIN"
    DEVELOPER = "DEVELOPER"
    READ_ONLY = "READ_ONLY"

ROLE_PERMISSIONS: dict[Role, list[Permission]] = {
    Role.SUPER_ADMIN: [p for p in Permission],
    Role.ORG_OWNER: [
        Permission.MANAGE_ORG, Permission.VIEW_ORG, Permission.MANAGE_ORG_MEMBERS,
        Permission.MANAGE_PROJECT, Permission.VIEW_PROJECT,
        Permission.MANAGE_KEYS, Permission.VIEW_KEYS,
        Permission.MANAGE_ROUTING,
        Permission.VIEW_METRICS, Permission.VIEW_AUDIT
    ],
    Role.ORG_ADMIN: [
        Permission.VIEW_ORG, Permission.MANAGE_ORG_MEMBERS,
        Permission.MANAGE_PROJECT, Permission.VIEW_PROJECT,
        Permission.MANAGE_KEYS, Permission.VIEW_KEYS,
        Permission.MANAGE_ROUTING,
        Permission.VIEW_METRICS, Permission.VIEW_AUDIT
    ],
    Role.PROJECT_ADMIN: [
        Permission.MANAGE_PROJECT, Permission.VIEW_PROJECT,
        Permission.MANAGE_KEYS, Permission.VIEW_KEYS,
        Permission.MANAGE_ROUTING,
        Permission.VIEW_METRICS
    ],
    Role.DEVELOPER: [
        Permission.VIEW_PROJECT,
        Permission.VIEW_KEYS,
        Permission.VIEW_METRICS
    ],
    Role.READ_ONLY: [
        Permission.VIEW_PROJECT,
        Permission.VIEW_METRICS
    ]
}

def has_permission(user_role: Role, required_permission: Permission) -> bool:
    return required_permission in ROLE_PERMISSIONS.get(user_role, [])
