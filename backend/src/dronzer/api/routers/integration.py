from typing import Any

from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(
    prefix="/v1/integration",
    tags=["Integration Hub"],
    responses={404: {"description": "Not found"}},
)

class ConnectorRegistration(BaseModel):
    name: str
    type: str # e.g. "github", "jira", "mcp_remote"
    config: dict[str, Any]

@router.post("/connectors", status_code=status.HTTP_201_CREATED)
async def register_connector(req: ConnectorRegistration):
    """
    Registers a new Enterprise Connector or external MCP Server.
    """
    # Logic to validate credentials and save to database
    return {"id": "conn_123", "status": "registered", "type": req.type}

@router.get("/connectors")
async def list_connectors():
    """
    Lists all active Connectors in the organization.
    """
    return {
        "connectors": [
            {"id": "conn_github", "name": "GitHub Prod", "type": "github", "health": "ok"},
            {"id": "conn_mcp", "name": "Internal DB MCP", "type": "mcp_remote", "health": "degraded"}
        ]
    }

@router.get("/tools")
async def list_tools(category: str = None):
    """
    Lists all executable tools provided by registered Connectors.
    """
    # Merges all capabilities from local tools and remote MCP servers
    tools = [
        {"name": "extract_page_text", "connector": "browser_automation", "is_sandboxed": False},
        {"name": "create_pull_request", "connector": "github", "is_sandboxed": False}
    ]
    return {"tools": tools}

@router.get("/metrics")
async def get_tool_metrics():
    """
    Returns telemetry data for Tool Execution (Latency, Errors, Cost).
    """
    return {
        "extract_page_text": {"calls": 450, "avg_latency_ms": 1205.4, "error_rate": 0.02},
        "create_pull_request": {"calls": 12, "avg_latency_ms": 840.1, "error_rate": 0.0}
    }
