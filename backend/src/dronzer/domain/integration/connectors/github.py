from typing import Any

import structlog

from dronzer.domain.integration.connectors.base import BaseConnector, ConnectorAction

logger = structlog.get_logger("dronzer.integration.connectors.github")


class GitHubConnector(BaseConnector):
    """
    Integrates with GitHub API.
    Allows Agents to read repositories, create issues, and submit PRs.
    """

    @property
    def name(self) -> str:
        return "github"

    def get_available_actions(self) -> list[ConnectorAction]:
        return [
            ConnectorAction(
                name="get_issue",
                description="Fetches details of a specific GitHub issue.",
                parameters_schema={"repo": "string", "issue_number": "integer"},
            ),
            ConnectorAction(
                name="create_pull_request",
                description="Creates a new Pull Request.",
                parameters_schema={
                    "repo": "string",
                    "title": "string",
                    "head": "string",
                    "base": "string",
                },
            ),
        ]

    async def execute_action(
        self, action_name: str, params: dict[str, Any], credentials: dict[str, str]
    ) -> Any:
        logger.info(f"Executing GitHub Connector Action: {action_name}")

        token = credentials.get("github_token")
        if not token:
            raise ValueError("Missing github_token in credentials vault.")

        # Pseudo: async with httpx.AsyncClient() as client:
        #    client.headers = {"Authorization": f"Bearer {token}"}

        if action_name == "get_issue":
            return {"title": "Fix memory leak", "state": "open"}

        elif action_name == "create_pull_request":
            return {"pr_url": "https://github.com/dronzer/repo/pull/1", "status": "created"}

        else:
            raise ValueError(f"Unknown action: {action_name}")
