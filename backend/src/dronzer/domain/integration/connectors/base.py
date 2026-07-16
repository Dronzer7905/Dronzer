from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class ConnectorAction(BaseModel):
    name: str
    description: str
    parameters_schema: dict[str, Any]


class BaseConnector(ABC):
    """
    Abstract interface for integrating external 3rd party services
    (GitHub, Jira, Salesforce, PostgreSQL) into Dronzer.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def get_available_actions(self) -> list[ConnectorAction]:
        """Returns the list of capabilities this connector exposes to AI Agents."""
        pass

    @abstractmethod
    async def execute_action(
        self, action_name: str, params: dict[str, Any], credentials: dict[str, str]
    ) -> Any:
        """Executes a specific action against the remote service."""
        pass
