from collections.abc import Callable
from typing import Any

import structlog
from pydantic import BaseModel

logger = structlog.get_logger("dronzer.agents.tools")

class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters_schema: dict[str, Any]
    is_remote: bool = False # If true, delegates execution to an MCP Server

class ToolRegistry:
    """
    Central repository of Tools available for Agents.
    Integrates with the Model Context Protocol (MCP) to allow agents to securely 
    interact with external local or remote environments.
    """

    def __init__(self):
        self._tools: dict[str, ToolDefinition] = {}
        self._local_executors: dict[str, Callable] = {}

    def register_local_tool(self, tool_def: ToolDefinition, executor: Callable):
        """Registers a Python function as an executable tool."""
        self._tools[tool_def.name] = tool_def
        self._local_executors[tool_def.name] = executor
        logger.info(f"Registered Local Tool: {tool_def.name}")

    def register_mcp_server(self, server_url: str):
        """
        Connects to a remote MCP (Model Context Protocol) Server.
        Fetches the exposed tools from the server and adds them to this registry.
        """
        logger.info(f"Connecting to MCP Server at {server_url}")

        # Pseudo: response = httpx.get(f"{server_url}/mcp/tools")
        # For each tool in response, register it with `is_remote=True`.
        pass

    def get_available_tools(self, allowed_tool_ids: list[str]) -> list[ToolDefinition]:
        """
        Returns a list of tool JSON schemas for injection into the LLM context.
        Filtered by the Agent's RBAC allowed_tools list.
        """
        if "*" in allowed_tool_ids:
            return list(self._tools.values())

        return [t for t in self._tools.values() if t.name in allowed_tool_ids]

    async def execute_tool(self, tool_name: str, parameters: dict[str, Any]) -> Any:
        """
        Executes a specific tool requested by the LLM.
        """
        tool_def = self._tools.get(tool_name)
        if not tool_def:
            raise ValueError(f"Tool {tool_name} not found in Registry.")

        logger.debug(f"Executing Tool {tool_name}", parameters=parameters)

        if tool_def.is_remote:
            # Delegate to the remote MCP Server
            # return httpx.post(f"{mcp_url}/execute/{tool_name}", json=parameters)
            return {"status": "success", "mcp_response": "Mock remote execution"}
        else:
            # Execute local python callable
            executor = self._local_executors[tool_name]
            return await executor(**parameters)
