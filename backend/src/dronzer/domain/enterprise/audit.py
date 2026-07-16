import uuid
from datetime import UTC, datetime
from typing import Any

import structlog
from pydantic import BaseModel

logger = structlog.get_logger("dronzer.enterprise.audit")


class AuditEvent(BaseModel):
    """
    Standard schema for immutable audit logs.
    Essential for SOC2, HIPAA, and ISO 27001 compliance.
    """

    event_id: str
    timestamp: str
    action: str  # e.g. "api_key.created", "policy.updated", "user.login"
    actor_id: str  # User ID or Service Account ID
    organization_id: str
    target_resource_id: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    metadata: dict[str, Any] = {}  # e.g. {"changes": {"previous": "X", "new": "Y"}}


class AuditLogger:
    """
    Captures and sinks enterprise audit events.
    In production, this should sink to an append-only datastore like
    Elasticsearch, AWS CloudWatch, or a dedicated WORM (Write Once Read Many) bucket.
    """

    def __init__(self, event_bus: Any = None):
        self.event_bus = event_bus

    async def log_action(self, action: str, actor_id: str, organization_id: str, **kwargs) -> str:
        """
        Records a compliance event.
        """
        event = AuditEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(UTC).isoformat(),
            action=action,
            actor_id=actor_id,
            organization_id=organization_id,
            target_resource_id=kwargs.get("target_resource_id"),
            ip_address=kwargs.get("ip_address"),
            user_agent=kwargs.get("user_agent"),
            metadata=kwargs.get("metadata", {}),
        )

        # Log locally as JSON for standard ingest (Fluentd/Datadog)
        logger.info("AUDIT_EVENT", **event.model_dump())

        # If event bus is configured, publish for real-time alerting (e.g. SIEM integrations)
        if self.event_bus:
            # await self.event_bus.publish("audit.events", event.model_dump())
            pass

        return event.event_id
