from typing import Any

import structlog
from pydantic import BaseModel

logger = structlog.get_logger("dronzer.enterprise.billing")


class PricingModel(BaseModel):
    """Defines the cost of tokens for a specific AI model."""

    model_id: str
    prompt_token_cost_usd_per_1k: float
    completion_token_cost_usd_per_1k: float


class InvoiceRecord(BaseModel):
    organization_id: str
    billing_period: str  # e.g. "2026-07"
    total_usd: float
    line_items: list[dict[str, Any]]


class BillingEngine:
    """
    Tracks token consumption, maps it to pricing matrices, and calculates costs.
    Supports organization-level billing and project-level chargebacks.
    """

    def __init__(self):
        # In a real app, this would be fetched from the DB/Stripe
        self._pricing_cache: dict[str, PricingModel] = {
            "gpt-4": PricingModel(
                model_id="gpt-4",
                prompt_token_cost_usd_per_1k=0.03,
                completion_token_cost_usd_per_1k=0.06,
            ),
            "gpt-3.5-turbo": PricingModel(
                model_id="gpt-3.5-turbo",
                prompt_token_cost_usd_per_1k=0.0015,
                completion_token_cost_usd_per_1k=0.002,
            ),
        }

    def calculate_cost(self, model_id: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculates the exact USD cost of a specific inference request."""
        pricing = self._pricing_cache.get(model_id)
        if not pricing:
            logger.warning("Pricing not found for model. Defaulting to 0.", model=model_id)
            return 0.0

        prompt_cost = (prompt_tokens / 1000.0) * pricing.prompt_token_cost_usd_per_1k
        completion_cost = (completion_tokens / 1000.0) * pricing.completion_token_cost_usd_per_1k

        return prompt_cost + completion_cost

    def generate_monthly_invoice(self, organization_id: str, current_month: str) -> InvoiceRecord:
        """
        Aggregates all usage records for an Organization into a monthly invoice.
        Used for Stripe sync or internal chargebacks.
        """
        logger.info("Generating invoice for organization", org=organization_id, month=current_month)

        # Pseudo-logic: query DB for all usage events in `current_month` for this `org_id`
        # Group by `model_id` or `project_id` to generate line items.

        return InvoiceRecord(
            organization_id=organization_id,
            billing_period=current_month,
            total_usd=124.50,  # Simulated aggregated cost
            line_items=[
                {"project": "Prod-App", "model": "gpt-4", "cost_usd": 100.00},
                {"project": "Dev-App", "model": "gpt-3.5-turbo", "cost_usd": 24.50},
            ],
        )
