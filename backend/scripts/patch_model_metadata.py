"""
patch_model_metadata.py
=======================
Patches the capabilities JSON field of models in the DB with metadata from the CSV.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from dronzer.infrastructure.database.core import get_db_session, engine
from dronzer.infrastructure.database.models.ai import Model
from sqlalchemy import select

METADATA = {
    # GROQ
    "llama-3.1-8b-instant": {"rate_limit": "~30 RPM / 6000 TPM", "daily_cap": "~14400 req/day", "notes": "Fastest small model on LPU hardware; genuinely free - no credits system", "is_preview": False, "chat": True, "code": True, "json_mode": True, "vision": False, "reasoning": False},
    "llama-3.3-70b-versatile": {"rate_limit": "~30 RPM / 6000 TPM", "daily_cap": "~1000 req/day", "notes": "Best general-purpose free model on Groq", "is_preview": False, "chat": True, "code": True, "json_mode": True, "vision": False, "reasoning": False},
    "openai/gpt-oss-120b": {"rate_limit": "~30 RPM / 6000 TPM", "daily_cap": "~1000 req/day", "notes": "OpenAI open-weight flagship; built-in browser search + code execution", "is_preview": False, "chat": True, "code": True, "json_mode": True, "vision": False, "reasoning": False},
    "openai/gpt-oss-20b": {"rate_limit": "~30 RPM / 6000 TPM", "daily_cap": "~1000 req/day", "notes": "Smaller/faster GPT-OSS variant (~1000 tok/sec)", "is_preview": False, "chat": True, "code": True, "json_mode": False, "vision": False, "reasoning": False},
    "groq/compound": {"rate_limit": "200 RPM / 200K TPM", "daily_cap": "N/A", "notes": "Agentic system with built-in web search + code execution tools", "is_preview": False, "chat": True, "code": True, "json_mode": False, "vision": False, "reasoning": False, "agentic": True},
    "groq/compound-mini": {"rate_limit": "200 RPM / 200K TPM", "daily_cap": "N/A", "notes": "Lighter agentic system variant", "is_preview": False, "chat": True, "code": False, "json_mode": False, "vision": False, "reasoning": False, "agentic": True},
    "meta-llama/llama-4-scout-17b-16e-instruct": {"rate_limit": "Preview tier - lower/variable RPM", "daily_cap": "N/A", "notes": "PREVIEW - evaluation only; can be pulled with no notice", "is_preview": True, "chat": True, "code": False, "json_mode": False, "vision": False, "reasoning": False},
    "qwen/qwen3-32b": {"rate_limit": "Preview tier - lower/variable RPM", "daily_cap": "N/A", "notes": "PREVIEW - reasoning model; evaluation only", "is_preview": True, "chat": True, "code": False, "json_mode": False, "vision": False, "reasoning": True},

    # GOOGLE AI STUDIO
    "gemini-2.5-flash": {"rate_limit": "~10-15 RPM", "daily_cap": "~250-1500 RPD", "notes": "Best all-round free model; multimodal", "is_preview": False, "chat": True, "code": True, "json_mode": True, "vision": True, "reasoning": False},
    "gemini-2.5-flash-lite": {"rate_limit": "~15 RPM", "daily_cap": "~1000-1500 RPD", "notes": "Lightweight cheapest-quota variant", "is_preview": False, "chat": True, "code": True, "json_mode": True, "vision": True, "reasoning": False},
    "gemini-3-flash": {"rate_limit": "~10 RPM", "daily_cap": "Lower RPD than 2.5", "notes": "Latest flagship-speed model", "is_preview": False, "chat": True, "code": True, "json_mode": True, "vision": True, "reasoning": False},
    "gemini-3.1-flash-lite": {"rate_limit": "~15 RPM", "daily_cap": "Higher RPD (most generous)", "notes": "GA since May 2026", "is_preview": False, "chat": True, "code": True, "json_mode": True, "vision": True, "reasoning": False},
    "text-embedding-004": {"rate_limit": "Free on free tier", "daily_cap": "N/A", "notes": "Embeddings model - useful for RAG pipelines", "is_preview": False, "chat": False, "code": False, "json_mode": False, "vision": False, "reasoning": False, "embedding": True},

    # MISTRAL
    "mistral-small-latest": {"rate_limit": "~1-2 RPS (Experiment mode)", "daily_cap": "Rate-limited", "notes": "Free MODE - phone verification required", "is_preview": False, "chat": True, "code": False, "json_mode": True, "vision": False, "reasoning": False},
    "mistral-medium-latest": {"rate_limit": "~1-2 RPS (Experiment mode)", "daily_cap": "Rate-limited", "notes": "Runs on same $0 Free mode as Small", "is_preview": False, "chat": True, "code": False, "json_mode": True, "vision": False, "reasoning": False},
    "codestral-latest": {"rate_limit": "~1-2 RPS (Experiment mode)", "daily_cap": "Rate-limited", "notes": "Coding-specialist model under Free mode", "is_preview": False, "chat": True, "code": True, "json_mode": False, "vision": False, "reasoning": False},
    "devstral-small-latest": {"rate_limit": "~1-2 RPS (Experiment mode)", "daily_cap": "Rate-limited", "notes": "Lightweight open coding-agent model", "is_preview": False, "chat": True, "code": True, "json_mode": False, "vision": False, "reasoning": False},
    "labs-leanstral-2603": {"rate_limit": "Explicitly $0/Free (no Experiment-mode gating)", "daily_cap": "Limited period", "notes": "Lean 4 formal-proof coding agent - niche", "is_preview": False, "chat": False, "code": True, "json_mode": False, "vision": False, "reasoning": True},

    # CEREBRAS
    "gpt-oss-120b": {"rate_limit": "~30 RPM", "daily_cap": "1,000,000 tokens/day", "notes": "Only PRODUCTION model on Cerebras free endpoint", "is_preview": False, "chat": True, "code": True, "json_mode": False, "vision": False, "reasoning": False},
    "gemma-4-31b": {"rate_limit": "~30 RPM", "daily_cap": "1,000,000 tokens/day", "notes": "PREVIEW model - eval only - can vanish with no notice", "is_preview": True, "chat": True, "code": False, "json_mode": False, "vision": False, "reasoning": False},
    "zai-glm-4.7": {"rate_limit": "~30 RPM", "daily_cap": "1,000,000 tokens/day", "notes": "PREVIEW model", "is_preview": True, "chat": True, "code": False, "json_mode": False, "vision": False, "reasoning": False},

    # CLOUDFLARE WORKERS AI
    "@cf/meta/llama-3.1-8b-instruct": {"rate_limit": "Shared 10K neuron/day pool", "daily_cap": "~15-25 calls/day (shared pool)", "notes": "Neurons shared across ALL models - not per-model", "is_preview": False, "chat": True, "code": False, "json_mode": False, "vision": False, "reasoning": False},
    "@cf/meta/llama-3.2-3b-instruct": {"rate_limit": "Shared 10K neuron/day pool", "daily_cap": "Shared pool", "notes": "Cheaper-per-call than 8B model", "is_preview": False, "chat": True, "code": False, "json_mode": False, "vision": False, "reasoning": False},
    "@cf/mistral/mistral-7b-instruct-v0.2": {"rate_limit": "Shared 10K neuron/day pool", "daily_cap": "Shared pool", "notes": "Small efficient model", "is_preview": False, "chat": True, "code": False, "json_mode": False, "vision": False, "reasoning": False},
    "@cf/qwen/qwen2.5-7b-instruct": {"rate_limit": "Shared 10K neuron/day pool", "daily_cap": "Shared pool", "notes": "Small Alibaba model", "is_preview": False, "chat": True, "code": True, "json_mode": False, "vision": False, "reasoning": False},
    "@cf/google/gemma-3-12b-it": {"rate_limit": "Shared 10K neuron/day pool", "daily_cap": "Shared pool", "notes": "Google open model", "is_preview": False, "chat": True, "code": False, "json_mode": False, "vision": False, "reasoning": False},
    "@cf/deepseek-ai/deepseek-r1-distill-qwen-32b": {"rate_limit": "Shared 10K neuron/day pool", "daily_cap": "Shared pool", "notes": "Reasoning-distilled model", "is_preview": False, "chat": True, "code": False, "json_mode": False, "vision": False, "reasoning": True},

    # OPENROUTER
    "qwen/qwen3-coder:free": {"rate_limit": "20 RPM", "daily_cap": "50/day (unfunded) or 1000/day ($10 top-up)", "notes": "Strongest free coding model on OpenRouter", "is_preview": False, "chat": True, "code": True, "json_mode": True, "vision": False, "reasoning": False},
    "deepseek/deepseek-r1:free": {"rate_limit": "20 RPM", "daily_cap": "50/day or 1000/day", "notes": "Reasoning model", "is_preview": False, "chat": True, "code": False, "json_mode": False, "vision": False, "reasoning": True},
    "deepseek/deepseek-chat-v3.1:free": {"rate_limit": "20 RPM", "daily_cap": "50/day or 1000/day", "notes": "General flagship-class chat", "is_preview": False, "chat": True, "code": True, "json_mode": True, "vision": False, "reasoning": False},
    "meta-llama/llama-3.3-70b-instruct:free": {"rate_limit": "20 RPM", "daily_cap": "50/day or 1000/day", "notes": "Solid general-purpose free model", "is_preview": False, "chat": True, "code": True, "json_mode": False, "vision": False, "reasoning": False},
    "meta-llama/llama-4-maverick:free": {"rate_limit": "20 RPM", "daily_cap": "50/day or 1000/day", "notes": "Meta's 400B MoE flagship (17B active) - multimodal", "is_preview": False, "chat": True, "code": False, "json_mode": False, "vision": True, "reasoning": False},
    "openai/gpt-oss-120b:free": {"rate_limit": "20 RPM", "daily_cap": "50/day or 1000/day", "notes": "OpenAI open-weight model", "is_preview": False, "chat": True, "code": True, "json_mode": True, "vision": False, "reasoning": False},
    "openai/gpt-oss-20b:free": {"rate_limit": "20 RPM", "daily_cap": "50/day or 1000/day", "notes": "Smaller GPT-OSS variant", "is_preview": False, "chat": True, "code": True, "json_mode": False, "vision": False, "reasoning": False},
    "z-ai/glm-4.5-air:free": {"rate_limit": "20 RPM", "daily_cap": "50/day or 1000/day", "notes": "Zhipu GLM lightweight variant", "is_preview": False, "chat": True, "code": False, "json_mode": False, "vision": False, "reasoning": False},
    "nvidia/nemotron-3-ultra:free": {"rate_limit": "20 RPM", "daily_cap": "50/day or 1000/day", "notes": "1M-context agent tasks while promo lasts - NVIDIA has pulled free models before", "is_preview": True, "chat": True, "code": False, "json_mode": False, "vision": False, "reasoning": False},
    "openrouter/free": {"rate_limit": "20 RPM", "daily_cap": "50/day or 1000/day", "notes": "Auto-router picks a working free model for you", "is_preview": False, "chat": True, "code": False, "json_mode": False, "vision": False, "reasoning": False},

    # NVIDIA NIM
    "meta/llama-3.3-70b-instruct": {"rate_limit": "~40 RPM (account-level)", "daily_cap": "No fixed cap", "notes": "CAVEAT: verify current behavior - some report depleting credit pools", "is_preview": False, "chat": True, "code": True, "json_mode": False, "vision": False, "reasoning": False},
    "deepseek-ai/deepseek-r1": {"rate_limit": "~40 RPM", "daily_cap": "No fixed cap", "notes": "Reasoning model; larger models may be more rate-limited", "is_preview": False, "chat": True, "code": False, "json_mode": False, "vision": False, "reasoning": True},
    "qwen/qwen3-coder-480b-a35b-instruct": {"rate_limit": "~40 RPM", "daily_cap": "No fixed cap", "notes": "Agentic coding model", "is_preview": False, "chat": True, "code": True, "json_mode": False, "vision": False, "reasoning": False},
    "google/gemma-3-27b-it": {"rate_limit": "~40 RPM", "daily_cap": "No fixed cap", "notes": "Google open model on NVIDIA infra", "is_preview": False, "chat": True, "code": False, "json_mode": False, "vision": False, "reasoning": False},
    "nvidia/nemotron-mini-4b-instruct": {"rate_limit": "~40 RPM", "daily_cap": "No fixed cap", "notes": "NVIDIA's own small model - most reliably free-tier", "is_preview": False, "chat": True, "code": False, "json_mode": False, "vision": False, "reasoning": False},
    "mistralai/mistral-large-3": {"rate_limit": "~40 RPM", "daily_cap": "No fixed cap", "notes": "Mistral's flagship hosted free via NVIDIA - different from Mistral's own throttled Free mode", "is_preview": False, "chat": True, "code": True, "json_mode": True, "vision": False, "reasoning": False},
}

async def patch():
    print("\\nDronzer -- Patching Model Metadata")
    print("=" * 54)
    
    updated = 0
    not_found = 0
    
    async for session in get_db_session():
        for name, meta in METADATA.items():
            result = await session.execute(select(Model).where(Model.name == name))
            models = result.scalars().all()
            if not models:
                print(f"  [MISSING] {name}")
                not_found += 1
                continue
                
            for m in models:
                # Merge existing capabilities with new metadata
                new_caps = m.capabilities.copy() if m.capabilities else {}
                new_caps.update(meta)
                m.capabilities = new_caps
                updated += 1
                print(f"  [OK]      Patched {name}")
                
        await session.commit()
        break
        
    await engine.dispose()
    
    print("=" * 54)
    print(f"  Models updated: {updated}")
    print(f"  Models missing: {not_found}")
    print("  Done!")

if __name__ == "__main__":
    asyncio.run(patch())
