import uuid
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

import structlog
from pydantic import BaseModel

logger = structlog.get_logger("dronzer.enterprise.workflows")


class WorkflowStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class ApprovalRequest(BaseModel):
    """Represents a human-in-the-loop approval ticket."""

    request_id: str
    organization_id: str
    requester_id: str
    action: str  # e.g., "rotate_provider_secret"
    payload: dict[str, Any]
    status: WorkflowStatus
    approver_roles_required: list[str]
    created_at: str


class ApprovalWorkflowEngine:
    """
    Manages multi-step asynchronous approvals for sensitive operations.
    Examples: Adding a new model, changing a global policy, viewing a secret.
    """

    def __init__(self, db_session: Any = None):
        self.db = db_session

    async def create_request(
        self,
        org_id: str,
        requester_id: str,
        action: str,
        payload: dict[str, Any],
        roles_required: list[str],
    ) -> str:
        """Generates a new approval ticket and sets it to PENDING."""
        req = ApprovalRequest(
            request_id=str(uuid.uuid4()),
            organization_id=org_id,
            requester_id=requester_id,
            action=action,
            payload=payload,
            status=WorkflowStatus.PENDING,
            approver_roles_required=roles_required,
            created_at=datetime.now(UTC).isoformat(),
        )
        # Store to DB...
        logger.info("Approval Request Created", request_id=req.request_id, action=action)

        # Trigger notification (Slack/Email) to approvers
        return req.request_id

    async def review_request(self, request_id: str, reviewer_id: str, approved: bool) -> bool:
        """
        Processes a reviewer's decision.
        If approved, the Gateway should execute the requested `action`.
        """
        # Fetch request from DB...
        status = WorkflowStatus.APPROVED if approved else WorkflowStatus.REJECTED
        logger.info(
            "Approval Request Reviewed",
            request_id=request_id,
            status=status.value,
            reviewer=reviewer_id,
        )

        # If approved, dispatch the payload to the actual execution handler (e.g. Vault rotation)
        return approved
