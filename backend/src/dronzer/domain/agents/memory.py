from typing import Any

import structlog

from dronzer.domain.knowledge.memory_engine import MemoryEngine

logger = structlog.get_logger("dronzer.agents.memory")


class SharedTeamMemory:
    """
    Provides a shared memory context for a Multi-Agent team.
    Integrates with the RAG Knowledge Platform to persist long-term agent memories.
    """

    def __init__(self, memory_engine: MemoryEngine, session_id: str):
        self.memory_engine = memory_engine
        self.session_id = session_id
        self._working_memory: list[dict[str, Any]] = []

    async def add_fact(self, agent_name: str, fact: str):
        """
        An agent discovers a fact and broadcasts it to the Shared Working Memory.
        """
        logger.debug(f"Agent {agent_name} added fact to shared memory.")
        self._working_memory.append({"source": agent_name, "fact": fact})

        # Persist to Long-Term RAG memory asynchronously
        await self.memory_engine.add_turn(
            self.session_id, role="system", content=f"[{agent_name} discovered]: {fact}"
        )

    async def get_working_memory_context(self) -> str:
        """
        Compiles the current shared scratchpad for injection into an Agent's prompt.
        """
        if not self._working_memory:
            return "No shared team facts established yet."

        context = "Shared Team Memory:\n"
        for item in self._working_memory:
            context += f"- {item['source']}: {item['fact']}\n"

        return context

    async def search_long_term_knowledge(self, query: str) -> list[str]:
        """
        Allows an agent to semantically search the team's historical memory.
        """
        logger.info("Searching long-term shared team memory.", query=query)
        return await self.memory_engine.search_long_term_memory(self.session_id, query)
