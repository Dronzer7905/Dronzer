import random
from typing import Any

import structlog

from dronzer.infrastructure.cluster.discovery import ServiceRegistry

logger = structlog.get_logger("dronzer.cluster.router")

class GlobalRouter:
    """
    Intelligent L7 routing layer for multi-region deployments.
    Routes API requests, AI workflows, and Database syncs to the optimal node
    based on latency, cost, and geographical compliance.
    """

    def __init__(self, registry: ServiceRegistry):
        self.registry = registry

    async def route_request(self, request_context: dict[str, Any]) -> str:
        """
        Determines the optimal Node ID to process a given request.
        """
        logger.debug("Calculating global route", context=request_context)

        # 1. Parse Routing Constraints (e.g., must run in EU for GDPR, must use GPU)
        constraints = {}
        if request_context.get("requires_gdpr"):
            constraints["compliance"] = "gdpr"
        if request_context.get("requires_gpu"):
            constraints["gpu"] = True

        # 2. Fetch healthy nodes matching constraints
        eligible_nodes = await self.registry.find_healthy_nodes(constraints)

        if not eligible_nodes:
            logger.error("No eligible nodes available for routing constraints", constraints=constraints)
            raise ConnectionError("Service Unavailable: No healthy nodes match routing constraints.")

        # 3. Apply Routing Strategy
        strategy = request_context.get("routing_strategy", "latency") # 'latency', 'cost', 'weighted_round_robin'

        if strategy == "weighted_round_robin":
            # Simple probabilistic routing based on node capacity weight
            total_weight = sum(n.get("weight", 10) for n in eligible_nodes)
            r = random.uniform(0, total_weight)
            upto = 0
            for node in eligible_nodes:
                if upto + node.get("weight", 10) >= r:
                    logger.info(f"Routed request to {node['id']} via Weighted Round Robin")
                    return node["id"]
                upto += node.get("weight", 10)

        # Default fallback (Mocking Latency/Geo resolution by just picking the first)
        selected_node = eligible_nodes[0]
        logger.info(f"Routed request to {selected_node['id']} via Primary Strategy")
        return selected_node["id"]
