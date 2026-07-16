from typing import Any

import structlog

logger = structlog.get_logger("dronzer.integration.gateways.adapters")


class ProtocolAdapter:
    """
    Translates various external API protocols (REST, GraphQL, gRPC)
    into a unified internal Event or Tool Call format.
    Allows Dronzer to expose its Agents and Workflows over any protocol.
    """

    async def translate_rest_to_event(
        self, request_method: str, path: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Translates an incoming HTTP REST call into an internal Workflow/Agent trigger event.
        """
        logger.debug(f"Translating REST request: {request_method} {path}")
        return {"source_protocol": "REST", "event_type": "webhook_trigger", "payload": payload}

    async def translate_graphql_to_event(
        self, query: str, variables: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Translates a GraphQL query into an internal request.
        """
        logger.debug("Translating GraphQL request")
        return {
            "source_protocol": "GraphQL",
            "event_type": "query_trigger",
            "payload": {"query": query, "variables": variables},
        }
