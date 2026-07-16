from typing import Any

import structlog

from dronzer.domain.enterprise.rbac import PolicyEngine
from dronzer.domain.integration.mcp.server import MCPServer

logger = structlog.get_logger("dronzer.integration.mcp.gateway")


class MCPGateway:
    """
    The secure entrypoint for all Model Context Protocol (MCP) traffic.
    Authenticates incoming SSE requests, enforces Organization Policies via RBAC,
    and bridges the traffic to the internal MCPServer engine.
    """

    def __init__(self, mcp_server: MCPServer, policy_engine: PolicyEngine):
        self.mcp_server = mcp_server
        self.policy_engine = policy_engine

    async def handle_incoming_sse_request(
        self, api_key: str, rpc_payload: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Validates the request and routes it to the MCP Server.
        """
        logger.debug("Received MCP SSE Request via Gateway")

        # 1. Authenticate Request
        org_id = await self._authenticate(api_key)
        if not org_id:
            logger.error("MCP Authentication Failed")
            return {"isError": True, "error": {"code": -32000, "message": "Unauthorized"}}

        method = rpc_payload.get("method")

        # 2. Enforce Organization Level Policies (e.g. are they allowed to expose MCP tools?)
        is_allowed = self.policy_engine.evaluate_access(
            user_id=org_id, action="mcp_access", resource=method
        )

        if not is_allowed:
            logger.error("MCP Authorization Failed via Policy Engine")
            return {"isError": True, "error": {"code": -32000, "message": "Forbidden by Policy"}}

        # 3. Route to MCP Server Core
        params = rpc_payload.get("params", {})
        try:
            return await self.mcp_server.handle_rpc_request(method, params)
        except ValueError as e:
            return {"isError": True, "error": {"code": -32601, "message": str(e)}}
        except Exception:
            logger.exception("MCP Internal Gateway Error")
            return {"isError": True, "error": {"code": -32603, "message": "Internal Server Error"}}

    async def _authenticate(self, api_key: str) -> str | None:
        """
        Validates API key and returns the associated Organization ID.
        """
        # Mocking auth
        if api_key.startswith("dz_"):
            return "org_abc123"
        return None
