

class CostEngine:
    """
    Calculates cost estimations and verifies budget limits based on model pricing.
    """

    @staticmethod
    def estimate_cost(prompt_tokens: int, completion_tokens: int, model_pricing: dict[str, float]) -> float:
        """
        Estimates the total cost of a request based on per-1k token pricing.
        model_pricing should contain 'prompt_cost_per_1k' and 'completion_cost_per_1k'.
        """
        prompt_cost = model_pricing.get("prompt_cost_per_1k", 0.0)
        completion_cost = model_pricing.get("completion_cost_per_1k", 0.0)

        total_prompt = (prompt_tokens / 1000.0) * prompt_cost
        total_completion = (completion_tokens / 1000.0) * completion_cost

        return total_prompt + total_completion

    @staticmethod
    def enforce_budget(estimated_cost: float, remaining_budget: float) -> bool:
        """
        Checks if the estimated cost exceeds the tenant's remaining budget.
        """
        return estimated_cost <= remaining_budget
