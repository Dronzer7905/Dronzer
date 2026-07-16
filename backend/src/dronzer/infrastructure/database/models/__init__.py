from dronzer.infrastructure.database.base import Base
from dronzer.infrastructure.database.models.ai import (
    APIKey,
    APIKeyPool,
    Model,
    ModelGroup,
    Provider,
    ProviderGroup,
)
from dronzer.infrastructure.database.models.gateway import (
    GatewayKey,
)
from dronzer.infrastructure.database.models.routing import (
    CircuitBreaker,
    RetryPolicy,
    RoutingPolicy,
    RoutingRule,
)
from dronzer.infrastructure.database.models.system import (
    BackgroundJob,
    FeatureFlag,
    PluginConfiguration,
    PluginRegistry,
    Secret,
    SystemSetting,
)
from dronzer.infrastructure.database.models.telemetry import (
    AuditLog,
    KeyHealth,
    ModelHealth,
    ProviderHealth,
    RequestLog,
)
from dronzer.infrastructure.database.models.tenant import (
    Organization,
    Permission,
    Project,
    Role,
    User,
)

# Re-exporting Base so Alembic can find all models attached to it.
__all__ = [
    "Base",
    "Organization",
    "Project",
    "User",
    "Role",
    "Permission",
    "Provider",
    "ProviderGroup",
    "Model",
    "ModelGroup",
    "APIKey",
    "APIKeyPool",
    "GatewayKey",
    "RoutingPolicy",
    "RoutingRule",
    "RetryPolicy",
    "CircuitBreaker",
    "AuditLog",
    "RequestLog",
    "ProviderHealth",
    "ModelHealth",
    "KeyHealth",
    "SystemSetting",
    "PluginRegistry",
    "PluginConfiguration",
    "BackgroundJob",
    "FeatureFlag",
    "Secret",
]
