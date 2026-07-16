from typing import Any

import structlog

from dronzer.domain.workflows.dag import DAGCompiler
from dronzer.infrastructure.database.models.workflows.core import ExecutionStatus

logger = structlog.get_logger("dronzer.workflows.engine")


class WorkflowEngine:
    """
    The core runtime for Dronzer Workflows.
    Designed to run asynchronously within a Celery or Redis worker queue.
    Executes compiled DAGs step-by-step, managing variable state and human-in-the-loop pauses.
    """

    def __init__(self, db_session: Any = None):
        self.db = db_session
        self.node_registry = {}  # Mappings of string 'type' to actual Node Executor classes

    def register_node_executor(self, node_type: str, executor_class: Any):
        self.node_registry[node_type] = executor_class

    async def execute_workflow(
        self, execution_id: str, dag_definition: dict, initial_payload: dict
    ):
        """
        Main entrypoint for a background worker picking up a workflow job.
        """
        logger.info("Starting workflow execution", execution_id=execution_id)

        # 1. Compile and Validate the DAG
        compiler = DAGCompiler(dag_definition)
        try:
            compiler.validate()
        except ValueError as e:
            logger.error("DAG Validation Failed", error=str(e))
            await self._update_status(execution_id, ExecutionStatus.FAILED, str(e))
            return

        execution_order = compiler.get_execution_order()

        # 2. Fetch or Initialize State
        state = await self._load_state(execution_id) or {"global": initial_payload, "nodes": {}}

        # 3. Step through the topological order
        for node_id in execution_order:
            node_def = next(n for n in compiler.dag.nodes if n.id == node_id)

            # Skip if already completed (useful for resuming after a HITL pause)
            if state["nodes"].get(node_id, {}).get("status") == "COMPLETED":
                continue

            logger.debug("Executing node", node_id=node_id, node_type=node_def.type)

            # Resolve Executor
            executor_cls = self.node_registry.get(node_def.type)
            if not executor_cls:
                err = f"Unknown Node Type: {node_def.type}"
                logger.error(err)
                await self._update_status(execution_id, ExecutionStatus.FAILED, err)
                return

            executor = executor_cls()

            # Execute Node
            try:
                result = await executor.run(node_def.parameters, state)

                if result.get("_hitl_pause"):
                    # Node requested Human In The Loop approval
                    logger.info("Workflow paused for Human Approval", node_id=node_id)
                    state["nodes"][node_id] = {"status": "PAUSED"}
                    await self._save_state(
                        execution_id, state, ExecutionStatus.PAUSED, current_node=node_id
                    )
                    return  # Exit the background worker; waiting for REST API resume call

                # Update state with node outputs
                state["nodes"][node_id] = {"status": "COMPLETED", "outputs": result}
                state["global"].update(result)

            except Exception as e:
                logger.exception("Node execution failed", node_id=node_id, error=str(e))
                state["nodes"][node_id] = {"status": "FAILED", "error": str(e)}
                await self._save_state(execution_id, state, ExecutionStatus.FAILED)
                return

        # 4. Workflow Completed Successfully
        logger.info("Workflow execution completed successfully", execution_id=execution_id)
        await self._save_state(execution_id, state, ExecutionStatus.COMPLETED)

    # Database abstraction helpers
    async def _update_status(self, execution_id: str, status: ExecutionStatus, error: str = None):
        pass

    async def _load_state(self, execution_id: str) -> dict:
        return None

    async def _save_state(
        self, execution_id: str, state: dict, status: ExecutionStatus, current_node: str = None
    ):
        pass
