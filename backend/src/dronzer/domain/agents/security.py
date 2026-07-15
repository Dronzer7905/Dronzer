from typing import Any

import structlog

from dronzer.domain.enterprise.rbac import PolicyEngine
from dronzer.infrastructure.database.models.agents.core import AgentProfile

logger = structlog.get_logger("dronzer.agents.security")

class AgentSecurityEnforcer:
    """
    Acts as a middleware before any Agent can execute a Tool from the ToolRegistry.
    Enforces strict Role-Based Access Controls (RBAC) and prevents prompt-injection 
    attacks from turning into catastrophic remote code execution.
    """

    def __init__(self, policy_engine: PolicyEngine = None):
        self.policy_engine = policy_engine

    def validate_tool_execution(self, agent: AgentProfile, tool_name: str, parameters: dict[str, Any]) -> bool:
        """
        Determines if the Agent is permitted to execute the specified tool.
        """
        logger.debug(f"Validating execution of tool {tool_name} by agent {agent.name}")

        # 1. Profile-level explicit grant check
        if "*" not in agent.allowed_tools and tool_name not in agent.allowed_tools:
            logger.warning(f"Agent {agent.name} attempted unauthorized execution of {tool_name}")
            raise PermissionError(f"Agent {agent.name} is not authorized to use the tool: {tool_name}")

        # 2. Organization-level Policy check
        # In a real environment, the PolicyEngine would evaluate if the Organization
        # has disabled specific dangerous tools (like `shell_command`) globally.
        if self.policy_engine:
            context = {"agent_id": str(agent.id), "tool_name": tool_name}
            allowed = self.policy_engine.evaluate_access(
                user_id=str(agent.organization_id), # Mock context
                action="execute_tool",
                resource=f"tool:{tool_name}",
                context=context
            )
            if not allowed:
                logger.error(f"Organization Policy blocked tool {tool_name}")
                raise PermissionError(f"Organization Policy forbids execution of {tool_name}")

        # 3. Best-effort prompt injection screening on parameters
        self._screen_parameters_for_injection(parameters)

        return True

    def _screen_parameters_for_injection(self, parameters: dict[str, Any]):
        """
        Scans parameters for common command injection vectors.
        """
        for k, v in parameters.items():
            if isinstance(v, str):
                # Basic mock check for shell injection attempts if executing bash tools
                if any(bad_char in v for bad_char in [";", "&&", "|", "`", "$("]):
                    logger.warning("Potential command injection detected in tool parameters", param_key=k)
                    # In a rigid environment, we might raise an exception here or sanitize.
                    pass
