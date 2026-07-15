from typing import Any

import structlog

logger = structlog.get_logger("dronzer.orchestration.capability")


class CapabilityEngine:
    """
    Analyzes an incoming OpenAI-compatible payload to determine required AI capabilities.
    """

    @staticmethod
    def detect_capabilities(payload: dict[str, Any]) -> list[str]:
        """
        Parses the payload and returns a list of required capabilities.
        Example: ["chat", "vision", "json_mode"]
        """
        capabilities = ["chat"] # Default assumption for completions API

        # Detect Vision
        messages = payload.get("messages", [])
        for msg in messages:
            content = msg.get("content")
            if isinstance(content, list):
                for part in content:
                    if part.get("type") == "image_url":
                        capabilities.append("vision")
                        break

        # Detect JSON Mode
        response_format = payload.get("response_format", {})
        if response_format.get("type") == "json_object":
            capabilities.append("json_mode")

        # Detect Structured Outputs (JSON Schema)
        if response_format.get("type") == "json_schema":
            capabilities.append("structured_outputs")

        # Detect Tool Calling
        if "tools" in payload and payload["tools"]:
            capabilities.append("tool_calling")

        # Detect Embeddings (if hitting embeddings endpoint)
        if payload.get("input") and not payload.get("messages"):
            capabilities = ["embeddings"]

        # Deduplicate
        detected = list(set(capabilities))
        logger.debug("Detected capabilities", capabilities=detected)
        return detected

    @staticmethod
    def matches(required: list[str], provided: dict[str, bool]) -> bool:
        """
        Checks if a model's provided capabilities satisfy the request requirements.
        """
        for req in required:
            if not provided.get(req, False):
                return False
        return True
