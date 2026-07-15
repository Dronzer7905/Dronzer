# Dronzer AI Gateway — Decision Intelligence Engine

**Document Status:** ✅ Approved  
**Version:** 1.0  
**Approved Date:** July 8, 2026  

> Full document available in conversation artifacts. This is the permanent reference summary.

## Core Philosophy
- **Centralized Authority:** Every decision regarding routing, timeouts, retries, and API keys is made by this engine. No subsystem acts independently.
- **Deterministic Outcomes:** Given the same request, tenant state, and health state, the output is mathematically identical every time.
- **Explainability:** All routing decisions generate an auditable JSON trace detailing exactly why candidates were rejected or selected.

## Decision Pipeline
1. Build Request Context
2. Evaluate Hierarchical Policies (Overrides -> Project -> Org -> Global)
3. Filter Providers, Models, and Keys (Hard constraints)
4. Calculate Scores (Normalized math)
5. Rank and Select Winner
6. Attach Execution Strategy (Retries, Timeouts)
7. Return Immutable `ExecutionPlan`

## Performance & Extensibility
- **Pre-Filtering:** Eliminates invalid candidates before complex CPU scoring.
- **Memoization:** Identical contexts skip the pipeline and return cached Execution Plans instantly.
- **Plugin Hooks:** Extensions can filter candidates, alter scores, or mutate the final Execution Plan.
