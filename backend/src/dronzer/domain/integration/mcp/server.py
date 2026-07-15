from collections.abc import Callable
from typing import Any

import structlog
from pydantic import BaseModel

logger = structlog.get_logger("dronzer.integration.mcp.server")

class MCPTool(BaseModel):
    name: str
    description: str
    inputSchema: dict[str, Any]

class MCPResource(BaseModel):
    uri: str
    name: str
    mimeType: str

class MCPServer:
    """
    Implementation of the Model Context Protocol (MCP) Server.
    Allows external AI clients (like Claude Desktop) to connect to Dronzer 
    and leverage its registered tools, prompts, and resources.
    Supports JSON-RPC over both stdio and SSE (Server-Sent Events).
    """

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self._tools: dict[str, MCPTool] = {}
        self._tool_handlers: dict[str, Callable] = {}
        self._resources: dict[str, MCPResource] = {}
        self._resource_handlers: dict[str, Callable] = {}

    def register_tool(self, tool: MCPTool, handler: Callable):
        self._tools[tool.name] = tool
        self._tool_handlers[tool.name] = handler
        logger.debug(f"MCP Server '{self.name}' registered tool: {tool.name}")

    def register_resource(self, resource: MCPResource, handler: Callable):
        self._resources[resource.uri] = resource
        self._resource_handlers[resource.uri] = handler
        logger.debug(f"MCP Server '{self.name}' registered resource: {resource.uri}")

    async def handle_rpc_request(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        """
        Primary JSON-RPC router for the MCP Server.
        """
        logger.debug(f"MCP Server received RPC method: {method}")

        if method == "initialize":
            return {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "prompts": {},
                    "resources": {},
                    "tools": {}
                },
                "serverInfo": {
                    "name": self.name,
                    "version": self.version
                }
            }

        elif method == "tools/list":
            return {"tools": [t.dict() for t in self._tools.values()]}

        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            handler = self._tool_handlers.get(tool_name)

            if not handler:
                raise ValueError(f"Unknown tool: {tool_name}")

            try:
                result = await handler(**tool_args)
                return {"content": [{"type": "text", "text": str(result)}]}
            except Exception as e:
                return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

        elif method == "resources/list":
            return {"resources": [r.dict() for r in self._resources.values()]}

        elif method == "resources/read":
            uri = params.get("uri")
            handler = self._resource_handlers.get(uri)
            if not handler:
                raise ValueError(f"Unknown resource URI: {uri}")

            content = await handler()
            return {"contents": [{"uri": uri, "mimeType": self._resources[uri].mimeType, "text": content}]}

        else:
            raise ValueError(f"Unsupported MCP RPC method: {method}")
