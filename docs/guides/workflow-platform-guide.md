# Dronzer AI Gateway - Workflow & Agent Platform Guide

Welcome to the Dronzer Workflow & Agent Platform. This system allows you to compose visual Directed Acyclic Graphs (DAGs) out of intelligent nodes and delegate complex tasks to teams of autonomous AI Agents.

## Workflow Concepts
- **Workflow Templates**: Reusable JSON definitions of a DAG (Nodes and Edges).
- **Workflow Executions**: Instances of a Template, running asynchronously on background workers (Celery/Redis).
- **Nodes**: The building blocks of a workflow. Includes `LLMNode`, `HTTPRequestNode`, `ScriptNode`, and more.

## Building Autonomous Agents
Agents in Dronzer follow a ReAct (Reasoning + Acting) pattern.
1. Create an **Agent Profile** with a specific Role and System Prompt.
2. Grant the agent access to specific Tools via the **Tool Registry**.
3. (Optional) Define an **Agent Coordinator** (Supervisor) to break down large tasks and delegate them to a team of specialized Sub-Agents.

## Tool Registry & MCP
The Tool Registry is Model Context Protocol (MCP) compatible. You can register simple Python callables, or bind an Agent to an entire remote MCP Server, giving them instant access to databases, web searches, or internal corporate APIs. 
*Note: Tool execution is strictly guarded by the Enterprise RBAC Policy Engine.*

## Human-in-the-Loop (HITL)
To prevent rogue AI executions, insert an **Approval Node** into your Workflow. When the execution engine reaches this node, it will PAUSE the entire job, save the global state to the database, and dispatch a notification. The workflow will only resume once an Administrator hits the `/resume` REST endpoint.

## Debugging and Replay
If a workflow fails (e.g., rate limit exceeded or a script crashed), use the **Workflow Debugger**. You can view the timeline of inputs/outputs per node, patch the failed variables, and restart the execution precisely from the point of failure, saving tokens and time.
