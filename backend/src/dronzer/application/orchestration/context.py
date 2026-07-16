import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RequestContext:
    """
    Immutable snapshot of the incoming user request.
    Built at the very beginning of the pipeline.
    """

    tenant_id: uuid.UUID
    project_id: uuid.UUID | None
    user_id: uuid.UUID | None
    payload: dict[str, Any]
    headers: dict[str, str]

    # Pre-calculated attributes based on payload
    estimated_prompt_tokens: int = 0
    requested_model: str | None = None
    requested_capabilities: list[str] = field(default_factory=list)

    # Gateway Key Context
    gateway_key_id: uuid.UUID | None = None
    task_type: str = "chat"
    model_priorities: list[str] = field(default_factory=list)
    provider_priorities: list[str] = field(default_factory=list)


@dataclass
class DecisionContext:
    """
    State object passed around during the decision pipeline.
    Accumulates filters, scores, and the final execution plan.
    """

    request_context: RequestContext
    trace_id: uuid.UUID = field(default_factory=uuid.uuid4)

    # The active hierarchical policy to enforce
    active_policy: dict[str, Any] = field(default_factory=dict)

    # Candidates filtered down during evaluation
    valid_providers: list[uuid.UUID] = field(default_factory=list)
    valid_models: list[uuid.UUID] = field(default_factory=list)
    valid_keys: list[uuid.UUID] = field(default_factory=list)

    # Audit trail for explainability
    explanation_trace: list[dict[str, Any]] = field(default_factory=list)

    def log_decision(
        self, step: str, action: str, reason: str, metadata: dict[str, Any] | None = None
    ) -> None:
        """Appends a trace event for observability."""
        self.explanation_trace.append(
            {"step": step, "action": action, "reason": reason, "metadata": metadata or {}}
        )


@dataclass
class ExecutionPlan:
    """
    The deterministic output of the Decision Engine.
    The Pipeline blindly executes this plan.
    """

    primary_provider_id: uuid.UUID
    primary_model_id: uuid.UUID
    primary_key_id: uuid.UUID

    fallback_chain: list[dict[str, uuid.UUID]] = field(default_factory=list)

    timeout_ms: int = 60000
    max_retries: int = 3
    is_streaming: bool = False
