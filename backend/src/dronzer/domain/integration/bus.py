from collections.abc import Callable
from typing import Any

import structlog

logger = structlog.get_logger("dronzer.integration.bus")

class AgentMessageBus:
    """
    Distributed Pub/Sub communication bus for Multi-Agent systems.
    Allows agents running on separate hardware/workers to broadcast discovery packets, 
    send direct messages, and synchronize shared team memory.
    
    Designed to be backed by Redis Streams or Kafka.
    """

    def __init__(self, pubsub_engine: Any = None):
        self.engine = pubsub_engine
        self.subscriptions: dict[str, Callable] = {}

    async def broadcast_presence(self, agent_id: str, capabilities: list):
        """
        Agents announce their presence when they spin up.
        """
        logger.info(f"Agent {agent_id} broadcasting presence to network.")
        payload = {
            "type": "presence",
            "agent_id": agent_id,
            "capabilities": capabilities
        }
        await self._publish("dronzer.agents.discovery", payload)

    async def send_direct_message(self, from_agent: str, to_agent: str, content: str):
        """
        Sends a private message to a specific agent's inbox channel.
        """
        logger.debug(f"Direct message from {from_agent} to {to_agent}")
        payload = {
            "type": "direct_message",
            "from": from_agent,
            "content": content
        }
        await self._publish(f"dronzer.agents.inbox.{to_agent}", payload)

    async def subscribe(self, topic: str, callback: Callable):
        """
        Registers a callback to listen to a specific topic.
        """
        self.subscriptions[topic] = callback
        logger.debug(f"Subscribed to topic: {topic}")

    async def _publish(self, topic: str, payload: dict[str, Any]):
        """
        Internal publisher.
        """
        if self.engine:
            # e.g., await self.engine.xadd(topic, payload)
            pass
        else:
            # Mock local routing for development
            if topic in self.subscriptions:
                await self.subscriptions[topic](payload)
