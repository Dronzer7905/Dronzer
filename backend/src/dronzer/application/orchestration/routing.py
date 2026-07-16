import random
from typing import Protocol

from dronzer.application.orchestration.context import DecisionContext
from dronzer.infrastructure.database.models.ai import Model


class IRoutingStrategy(Protocol):
    """
    Interface for dynamic routing strategies.
    Strategies rank and sort the valid candidates.
    """

    def rank_models(self, context: DecisionContext, models: list[Model]) -> list[Model]: ...


class PriorityRouting(IRoutingStrategy):
    """Routes strictly based on a pre-defined priority list in the Tenant Policy."""

    def rank_models(self, context: DecisionContext, models: list[Model]) -> list[Model]:
        priorities = context.active_policy.get("model_priority", [])

        def get_priority(model: Model) -> int:
            try:
                return priorities.index(model.name)
            except ValueError:
                return 9999  # Lowest priority if not listed

        return sorted(models, key=get_priority)


class WeightedRouting(IRoutingStrategy):
    """Routes by distributing traffic based on percentage weights."""

    def rank_models(self, context: DecisionContext, models: list[Model]) -> list[Model]:
        # For simplicity in this implementation, we shuffle them to distribute load.
        # A true weighted router would use statistical distributions.
        shuffled = models[:]
        random.shuffle(shuffled)
        return shuffled


class CostOptimizedRouting(IRoutingStrategy):
    """Routes to the cheapest valid model capable of fulfilling the request."""

    def rank_models(self, context: DecisionContext, models: list[Model]) -> list[Model]:
        # Sort by completion cost (assuming capabilities JSON holds pricing data)
        def get_cost(model: Model) -> float:
            return model.capabilities.get("completion_cost_per_1k", 999.0)

        return sorted(models, key=get_cost)


class RoutingEngine:
    """
    Selects and executes the correct routing strategy based on the active policy.
    """

    def __init__(self):
        self.strategies = {
            "priority": PriorityRouting(),
            "weighted": WeightedRouting(),
            "cost_optimized": CostOptimizedRouting(),
        }

    def execute_strategy(self, context: DecisionContext, valid_models: list[Model]) -> list[Model]:
        strategy_name = context.active_policy.get("routing_strategy", "priority")
        strategy = self.strategies.get(strategy_name, PriorityRouting())

        context.log_decision(
            step="RoutingEngine",
            action="RankCandidates",
            reason=f"Executed {strategy_name} routing strategy",
            metadata={"candidate_count": len(valid_models)},
        )

        return strategy.rank_models(context, valid_models)
