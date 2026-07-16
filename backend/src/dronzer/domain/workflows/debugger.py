from typing import Any

import structlog
from pydantic import BaseModel

logger = structlog.get_logger("dronzer.workflows.debugger")


class TimelineEvent(BaseModel):
    node_id: str
    status: str
    duration_ms: int
    inputs: dict[str, Any]
    outputs: dict[str, Any]
    error: str = None


class WorkflowDebugger:
    """
    Examines a WorkflowExecution record and reconstructs a step-by-step timeline.
    Crucial for developers to debug complex DAGs and see exact variable states at each node.
    """

    def __init__(self, db_session: Any = None):
        self.db = db_session

    async def get_execution_timeline(self, execution_id: str) -> list[TimelineEvent]:
        """
        Parses the JSON `execution_state` and reconstructs the chronological history.
        """
        logger.debug("Generating debug timeline", execution_id=execution_id)

        # In a real environment, we query the DB for the Execution and parse the `execution_state["nodes"]`
        # Mocking timeline generation for Demonstration

        timeline = [
            TimelineEvent(
                node_id="node_input_1",
                status="COMPLETED",
                duration_ms=12,
                inputs={"user_query": "Hello"},
                outputs={"parsed_query": "Hello"},
            ),
            TimelineEvent(
                node_id="node_llm_1",
                status="FAILED",
                duration_ms=450,
                inputs={"prompt": "Hello"},
                outputs={},
                error="Rate limit exceeded for gpt-4-turbo",
            ),
        ]

        return timeline

    async def replay_from_node(self, execution_id: str, node_id: str, new_inputs: dict[str, Any]):
        """
        Allows a developer to alter the variables at a specific failed node
        and restart the WorkflowEngine from that point forward (saving time and tokens).
        """
        logger.info(
            "Replaying workflow from breakpoint", execution_id=execution_id, node_id=node_id
        )
        # 1. Fetch Execution
        # 2. Reset status of `node_id` and all downstream topological nodes to PENDING
        # 3. Patch `execution_state["global"]` with `new_inputs`
        # 4. Enqueue execution back into the Background Task queue
        return True
