# Dronzer AI Gateway - Universal AI Integration Layer

Welcome to the Dronzer Universal Integration Hub. This subsystem elevates Dronzer from a simple AI Gateway to a central nervous system for all Agentic communication, Tool executions, and enterprise integrations.

## The Model Context Protocol (MCP)
Dronzer fully supports Anthropic's Model Context Protocol in three distinct ways:
1. **MCP Server**: Dronzer exposes its own workflows, database schemas, and AI prompts to external clients (like Claude Desktop) via JSON-RPC over `stdio` or Server-Sent Events (`SSE`).
2. **MCP Client**: Dronzer Agents can query remote MCP servers hosted inside corporate firewalls, pulling in external tools automatically.
3. **MCP Gateway**: All incoming MCP traffic passes through the Dronzer RBAC Policy Engine, ensuring unauthorized clients cannot execute sensitive tools.

## Universal Tool Runtime & Sandboxing
To ensure arbitrary AI-generated code (Python, JS, Shell) does not compromise the host system, all script-based tools are executed inside the `SandboxEngine`. Currently, this relies on strict subprocess boundaries with timeouts, but it is architecturally designed to support Docker and Firecracker microVMs in production.

## Connectors & Browser Automation
The `connectors` package allows Dronzer to integrate natively with external systems.
- **Enterprise Connectors**: Native interfaces for GitHub, Jira, PostgreSQL, etc.
- **Headless Browser**: Built on Playwright, allowing Agents to open headless Chrome sessions, extract DOM text, fill forms, and take screenshots for vision-language models.

## Protocol Adapters & Message Bus
Dronzer unifies the world of AI communication:
- **Adapters**: Incoming REST, GraphQL, and gRPC requests are seamlessly translated into internal Dronzer Events.
- **Pub/Sub Bus**: Built for Redis Streams, allowing distributed Dronzer Agents running on separate hardware to broadcast discovery packets and pass messages to each other securely.
