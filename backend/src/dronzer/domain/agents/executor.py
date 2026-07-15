from typing import Any

import structlog

from dronzer.domain.agents.tools import ToolRegistry
from dronzer.infrastructure.database.models.agents.core import AgentProfile, AgentState

logger = structlog.get_logger("dronzer.agents.executor")

class AgentExecutor:
    """
    Executes a single Agent loop (ReAct pattern).
    1. Reads the system prompt and current AgentState (scratchpad).
    2. Calls the LLM with available tools.
    3. If LLM requests a tool, executes it and appends to scratchpad.
    4. Loops until LLM yields a final answer.
    """

    def __init__(self, agent_profile: AgentProfile, tool_registry: ToolRegistry, llm_provider: Any = None):
        self.profile = agent_profile
        self.tool_registry = tool_registry
        self.llm = llm_provider
        self.max_iterations = 10

    async def run(self, task_description: str, agent_state: AgentState) -> str:
        """
        Executes the main Agent loop to accomplish the task_description.
        """
        logger.info(f"Agent {self.profile.name} starting task execution.")

        # Determine available tools for this agent based on RBAC
        available_tools = self.tool_registry.get_available_tools(self.profile.allowed_tools)

        agent_state.current_goal = task_description
        iteration = 0

        while iteration < self.max_iterations:
            iteration += 1
            logger.debug(f"Agent ReAct Iteration {iteration}")

            # Construct context: System Prompt + Task + Scratchpad History
            context = self._build_context(task_description, agent_state)

            # Invoke LLM (Mocked)
            # llm_response = await self.llm.generate(context, tools=available_tools)
            llm_response = {"action": "final_answer", "content": "I have completed the task."}

            # Append LLM thought to scratchpad
            agent_state.scratchpad.append({"role": "assistant", "content": llm_response})

            if llm_response.get("action") == "final_answer":
                logger.info(f"Agent {self.profile.name} reached final answer.")
                return llm_response.get("content", "")

            elif llm_response.get("action") == "tool_call":
                # Execute requested tool
                tool_name = llm_response.get("tool_name")
                tool_args = llm_response.get("tool_args", {})

                try:
                    tool_result = await self.tool_registry.execute_tool(tool_name, tool_args)
                    # Append result to scratchpad for next iteration
                    agent_state.scratchpad.append({"role": "tool", "name": tool_name, "content": str(tool_result)})
                except Exception as e:
                    agent_state.scratchpad.append({"role": "tool", "name": tool_name, "error": str(e)})

        logger.warning(f"Agent {self.profile.name} hit max iterations ({self.max_iterations}).")
        return "Task failed: Agent hit maximum reasoning iterations."

    def _build_context(self, task: str, state: AgentState) -> list[dict[str, str]]:
        messages = [{"role": "system", "content": self.profile.system_prompt}]
        messages.append({"role": "user", "content": f"Task: {task}"})
        messages.extend(state.scratchpad)
        return messages
