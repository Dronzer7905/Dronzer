from typing import Any

import structlog
from pydantic import BaseModel

logger = structlog.get_logger("dronzer.enterprise.policy")

class PolicyViolationException(Exception):
    pass

class RequestContext(BaseModel):
    """Payload data representing the incoming inference request."""
    model: str
    provider: str
    max_tokens: int
    user_id: str
    project_id: str

class PolicyEngine:
    """
    Evaluates business and security rules defined by Organization Admins.
    Operates at the routing layer before requests hit the Provider SDK.
    """
    def __init__(self):
        pass

    def evaluate_request(self, request: RequestContext, tenant_policies: list[dict[str, Any]]):
        """
        Iterates over all configured policies for the tenant.
        Raises PolicyViolationException if any block condition is met.
        """
        for policy in tenant_policies:
            policy_type = policy.get("type")

            if policy_type == "block_model":
                blocked_models = policy.get("models", [])
                if request.model in blocked_models:
                    logger.warning("Policy Block: Model restricted", model=request.model, project=request.project_id)
                    raise PolicyViolationException(f"The model '{request.model}' is blocked by Organization policy.")

            elif policy_type == "max_tokens_cap":
                cap = policy.get("max_tokens", 0)
                if request.max_tokens > cap:
                    logger.warning("Policy Block: Max tokens exceeded cap", requested=request.max_tokens, cap=cap)
                    raise PolicyViolationException(f"Requested max_tokens ({request.max_tokens}) exceeds the policy cap of {cap}.")

            elif policy_type == "allowed_providers":
                allowed = policy.get("providers", [])
                if request.provider not in allowed:
                    logger.warning("Policy Block: Provider not allowed", provider=request.provider)
                    raise PolicyViolationException(f"Provider '{request.provider}' is not approved for this Organization.")

        logger.debug("Request passed all tenant policies.")
        return True
