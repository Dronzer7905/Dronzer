from typing import Any

import structlog

from dronzer.domain.enterprise.workflows import ApprovalWorkflowEngine
from dronzer.domain.workflows.nodes import BaseNodeExecutor

logger = structlog.get_logger("dronzer.workflows.hitl")

class ApprovalNodeExecutor(BaseNodeExecutor):
    """
    Suspends workflow execution until a human administrator reviews the state.
    Used for Human-in-the-Loop (HITL) scenarios (e.g., confirming a deployment or an AI generated email).
    """

    def __init__(self, approval_engine: ApprovalWorkflowEngine = None):
        self.approval_engine = approval_engine

    async def run(self, parameters: dict[str, Any], global_state: dict[str, Any]) -> dict[str, Any]:
        """
        Instead of completing, this node dispatches a notification and yields execution back to the worker.
        """
        logger.info("Encountered Human-in-the-Loop Approval Gate")

        roles_required = parameters.get("required_roles", ["admin"])
        context_message = parameters.get("message", "Workflow requires manual approval to proceed.")

        # In a real environment, we use the engine to persist an ApprovalRequest
        if self.approval_engine:
            org_id = global_state.get("organization_id", "default_org")
            requester_id = "workflow_engine"

            await self.approval_engine.create_request(
                org_id=org_id,
                requester_id=requester_id,
                action="workflow_node_approval",
                payload={"context": context_message, "state": global_state},
                roles_required=roles_required
            )

        # Returning `_hitl_pause: True` signals the WorkflowEngine to pause the background job
        # and persist state to the database as `PAUSED`.
        return {"_hitl_pause": True, "approval_message": context_message}
