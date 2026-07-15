from typing import Any

import structlog

logger = structlog.get_logger("dronzer.sdk.security")

class PluginSecuritySandbox:
    """
    Validates plugin configurations and sanitizes inputs before passing 
    them to dynamically loaded modules to prevent arbitrary execution exploits.
    """

    @staticmethod
    def validate_plugin_config(config: dict[str, Any]) -> bool:
        """
        Ensures the plugin configuration does not contain forbidden keys.
        """
        forbidden_keys = ["__class__", "__bases__", "__subclasses__", "eval", "exec"]
        for key in config.keys():
            if any(forbidden in key for forbidden in forbidden_keys):
                logger.error("Security violation: Forbidden key found in plugin config", key=key)
                return False
        return True

    @staticmethod
    def sanitize_payload(payload: dict[str, Any]) -> dict[str, Any]:
        """
        Strips potentially dangerous metadata from user payloads before handing 
        them to external SDKs or plugins.
        """
        safe_payload = payload.copy()
        # Ensure we don't pass internal gateway secrets if a user accidentally includes them
        if "_internal_auth" in safe_payload:
            del safe_payload["_internal_auth"]
        return safe_payload
