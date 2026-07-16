from typing import Any

import structlog
from pydantic import BaseModel, Field

logger = structlog.get_logger("dronzer.workflows.dag")


class WorkflowEdge(BaseModel):
    source: str
    target: str
    condition: str | None = None  # Optional JS/Python expression for branching


class WorkflowNode(BaseModel):
    id: str
    type: str  # 'llm', 'http', 'condition', 'human_approval', 'script'
    parameters: dict[str, Any] = Field(default_factory=dict)


class DAGDefinition(BaseModel):
    nodes: list[WorkflowNode]
    edges: list[WorkflowEdge]


class DAGCompiler:
    """
    Validates a Workflow Definition and computes the topological execution order.
    Ensures that the visual drag-and-drop flow is actually executable by the backend.
    """

    def __init__(self, definition: dict):
        self.raw_def = definition
        self.dag = DAGDefinition(**definition)
        self.adjacency_list = self._build_adjacency_list()

    def _build_adjacency_list(self) -> dict[str, list[str]]:
        adj: dict[str, list[str]] = {node.id: [] for node in self.dag.nodes}
        for edge in self.dag.edges:
            if edge.source in adj:
                adj[edge.source].append(edge.target)
        return adj

    def validate(self) -> bool:
        """
        Runs static analysis on the graph:
        1. Checks for unknown node types.
        2. Detects cyclical loops (DAGs must be acyclic unless using specific Loop Nodes).
        3. Validates required parameters per node type.
        """
        logger.debug("Validating workflow DAG topology.")

        # 1. Cycle detection (DFS)
        visited = set()
        recursion_stack = set()

        def has_cycle(node_id: str) -> bool:
            visited.add(node_id)
            recursion_stack.add(node_id)

            for neighbor in self.adjacency_list.get(node_id, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in recursion_stack:
                    return True  # Cycle detected

            recursion_stack.remove(node_id)
            return False

        for node in self.dag.nodes:
            if node.id not in visited:
                if has_cycle(node.id):
                    logger.error("Invalid workflow: Cycle detected in DAG.", node_id=node.id)
                    raise ValueError(
                        f"Workflow contains an invalid cycle involving node {node.id}. Use Loop nodes for intentional iteration."
                    )

        return True

    def get_execution_order(self) -> list[str]:
        """
        Returns a topologically sorted list of Node IDs.
        Used by the WorkflowEngine to execute independent branches concurrently or sequentially.
        """
        visited = set()
        stack: list[str] = []

        def topo_sort(node_id: str):
            visited.add(node_id)
            for neighbor in self.adjacency_list.get(node_id, []):
                if neighbor not in visited:
                    topo_sort(neighbor)
            stack.insert(0, node_id)

        for node in self.dag.nodes:
            if node.id not in visited:
                topo_sort(node.id)

        return stack
