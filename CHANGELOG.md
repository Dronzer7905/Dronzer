# Changelog

All notable changes to the Dronzer AI Gateway will be documented in this file.

## [2.0.0] - 2026-07-15

### Added
- **Task-Aware Routing Engine**: Built the `DecisionIntelligenceEngine` capable of analyzing tasks (Coding, Reasoning, JSON, Vision) and dynamically routing to the optimal LLM.
- **Resilient Failover**: Introduced the `FailoverEngine` and `RetryEngine` that seamlessly masks 429s and 500s from the user.
- **Provider Registry**: Integrated 45+ free and premium models across OpenAI, Anthropic, Gemini, Groq, Mistral, Cerebras, and OpenRouter.
- **UI Dashboard**: Built a beautiful, minimal Light Theme Next.js dashboard for API Key generation, tracking, and organization management.
- **OpenAI Compliance**: Fully compatible with the standard OpenAI API structure (`/v1/chat/completions`) for instant drop-in replacement in any app or IDE.

### Changed
- Refactored the core FastAPI backend from v1 to use a modular orchestrator pattern.
- Overhauled the frontend aesthetic to a minimalist Light Theme.

### Removed
- Deprecated v1 local SQLite database support in favor of a robust async PostgreSQL architecture.
