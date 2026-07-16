from typing import Any

import structlog

from dronzer.domain.agents.executor import AgentExecutor
from dronzer.infrastructure.database.models.agents.core import AgentState

logger = structlog.get_logger("dronzer.agents.collaboration")


class AgentCoordinator:
    """
    Acts as a Supervisor/Coordinator in a Multi-Agent system (similar to LangGraph Supervisor pattern).
    It receives a massive task, breaks it down, and delegates it to specialized sub-agents.
    """

    def __init__(self, supervisor_executor: AgentExecutor, sub_agents: dict[str, AgentExecutor]):
        self.supervisor = supervisor_executor
        self.sub_agents = sub_agents

    async def orchestrate(
        self, overarching_task: str, global_state: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Coordinates the execution of multiple agents to achieve a single goal.
        """
        logger.info(f"Coordinator {self.supervisor.profile.name} orchestrating Multi-Agent task.")

        # 1. Supervisor analyzes the task and generates a plan
        plan_state = AgentState(scratchpad=[])
        plan_prompt = f"Break down this task into sub-tasks for your team ({list(self.sub_agents.keys())}):\n{overarching_task}"

        delegation_plan_str = await self.supervisor.run(plan_prompt, plan_state)

        logger.debug(f"Delegation Plan Generated: {delegation_plan_str}")

        results: dict[str, Any] = {}

        # Mocking the parsed delegation plan for demonstration
        parsed_plan = [
            {"agent": "researcher_agent", "task": "Find market data"},
            {"agent": "writer_agent", "task": "Write the summary"},
        ]

        # 2. Execute sub-tasks sequentially (or concurrently depending on DAG)
        for step in parsed_plan:
            target_agent_name = step["agent"]
            sub_task = step["task"]

            executor = self.sub_agents.get(target_agent_name)
            if not executor:
                logger.warning(f"Requested agent {target_agent_name} not available in team.")
                continue

            logger.info(f"Delegating task to {target_agent_name}", task=sub_task)

            # Sub-agent execution
            sub_state = AgentState(
                scratchpad=[{"role": "system", "content": "Shared Context: " + str(results)}]
            )
            sub_result = await executor.run(sub_task, sub_state)

            results[target_agent_name] = sub_result

        # 3. Supervisor reviews final output
        review_state = AgentState(scratchpad=[])
        review_prompt = f"Compile the final answer based on your team's results: {results}"
        final_answer = await self.supervisor.run(review_prompt, review_state)

        logger.info("Multi-Agent Orchestration complete.")
        return {"status": "success", "final_output": final_answer, "team_results": results}
