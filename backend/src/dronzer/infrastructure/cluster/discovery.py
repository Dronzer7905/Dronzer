from typing import Any

import structlog

from dronzer.infrastructure.database.models.cluster.core import ClusterNode

logger = structlog.get_logger("dronzer.cluster.discovery")


class ServiceRegistry:
    """
    Provides Dynamic Discovery for Dronzer Services.
    Allows the Global Router to find healthy nodes across the global cluster
    that match specific capabilities (e.g. "needs GPU", "needs compliance=EU").
    """

    def __init__(self, db_session: Any = None, cache: Any = None):
        self.db = db_session
        self.cache = cache

    async def register_node(self, node: ClusterNode):
        """
        Announces a node's presence to the Service Registry.
        """
        logger.info(f"Registering Node in Service Registry: {node.hostname}")
        # Upsert Node in DB, then broadcast to Redis PubSub for immediate cache invalidation

    async def deregister_node(self, node_id: str):
        """
        Removes a node (graceful shutdown or missed heartbeat eviction).
        """
        logger.warning(f"Deregistering Node: {node_id}")

    async def find_healthy_nodes(self, required_capabilities: dict[str, Any] = None) -> list[dict]:
        """
        Queries the active pool of healthy nodes.
        Filters based on capabilities (e.g. requires specialized hardware for a specific LLM plugin).
        """
        logger.debug("Querying Service Registry for healthy nodes", filters=required_capabilities)

        # Mocking active nodes
        nodes = [
            {
                "id": "node_aws_useast1_01",
                "region": "us-east-1",
                "capabilities": {"gpu": True},
                "weight": 100,
            },
            {
                "id": "node_gcp_euwest3_02",
                "region": "eu-west-3",
                "capabilities": {"gpu": False, "compliance": "gdpr"},
                "weight": 50,
            },
        ]

        if not required_capabilities:
            return nodes

        filtered = []
        for n in nodes:
            match = True
            for k, v in required_capabilities.items():
                if n["capabilities"].get(k) != v:
                    match = False
                    break
            if match:
                filtered.append(n)

        return filtered
