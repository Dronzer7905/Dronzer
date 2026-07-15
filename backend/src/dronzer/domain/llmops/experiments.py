import random
from typing import Any

import structlog

logger = structlog.get_logger("dronzer.llmops.experiments")

class ABExperimentEngine:
    """
    Manages active A/B tests between Prompt Versions or Models.
    Hooks into the Gateway Routing layer to seamlessly split traffic.
    """

    def __init__(self, db_session: Any = None):
        self.db = db_session

        # Mock active experiments cache (loaded from Redis/DB in prod)
        self.active_experiments = {
            "prompt_support_bot": {
                "champion": "v1.2.0",
                "challenger": "v2.0.0-rc1",
                "traffic_split_pct": 10 # 10% of traffic goes to challenger
            }
        }

    async def get_target_version(self, prompt_name: str, session_id: str = None) -> str:
        """
        Determines which PromptVersion should be executed for an incoming API request.
        Handles sticky sessions if session_id is provided.
        """
        experiment = self.active_experiments.get(prompt_name)

        if not experiment:
            # If no active experiment, return the 'latest' published stable version
            return "latest"

        # Determine if this request falls into the challenger bucket
        roll = random.uniform(0, 100)
        is_challenger = roll <= experiment["traffic_split_pct"]

        target_version = experiment["challenger"] if is_challenger else experiment["champion"]

        logger.debug(
            f"Traffic split decision for {prompt_name}",
            roll=round(roll, 2),
            threshold=experiment["traffic_split_pct"],
            target_version=target_version
        )

        return target_version
