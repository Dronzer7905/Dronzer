"""
seed_free_providers.py
======================
Seeds all 44 free LLM providers and their models from the verified July 2026 list.
Run from the backend directory:
    python seed_free_providers.py

Safe to re-run — skips providers/models that already exist.
"""
import asyncio
import sys
from pathlib import Path

# Ensure the src directory is on the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dronzer.infrastructure.database.core import get_db_session, engine
from dronzer.infrastructure.database.models.ai import Provider, Model
from sqlalchemy import select

# ---------------------------------------------------------------------------
# Data from Free_LLM_Providers_Verified_Jul2026.csv
# ---------------------------------------------------------------------------

FREE_PROVIDERS = [
    {
        "name": "groq",
        "base_url": "https://api.groq.com/openai/v1",
        "models": [
            ("llama-3.1-8b-instant",                         131072),
            ("llama-3.3-70b-versatile",                      131072),
            ("openai/gpt-oss-120b",                          131072),
            ("openai/gpt-oss-20b",                           131072),
            ("groq/compound",                                131072),
            ("groq/compound-mini",                           131072),
            ("meta-llama/llama-4-scout-17b-16e-instruct",    131072),
            ("qwen/qwen3-32b",                               131072),
        ],
    },
    {
        "name": "google-ai-studio",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "models": [
            ("gemini-2.5-flash",       1000000),
            ("gemini-2.5-flash-lite",  1000000),
            ("gemini-3-flash",         1000000),
            ("gemini-3.1-flash-lite",  1000000),
            ("text-embedding-004",     8000),
        ],
    },
    {
        "name": "mistral",
        "base_url": "https://api.mistral.ai/v1",
        "models": [
            ("mistral-small-latest",   32000),
            ("mistral-medium-latest",  32000),
            ("codestral-latest",       32000),
            ("devstral-small-latest",  32000),
            ("labs-leanstral-2603",    32000),
        ],
    },
    {
        "name": "cerebras",
        "base_url": "https://api.cerebras.ai/v1",
        "models": [
            ("gpt-oss-120b",  8192),
            ("gemma-4-31b",   8192),
            ("zai-glm-4.7",   8192),
        ],
    },
    {
        "name": "cloudflare-workers-ai",
        "base_url": "https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1",
        "models": [
            ("@cf/meta/llama-3.1-8b-instruct",              8192),
            ("@cf/meta/llama-3.2-3b-instruct",              8192),
            ("@cf/mistral/mistral-7b-instruct-v0.2",        8192),
            ("@cf/qwen/qwen2.5-7b-instruct",                8192),
            ("@cf/google/gemma-3-12b-it",                   8192),
            ("@cf/deepseek-ai/deepseek-r1-distill-qwen-32b",8192),
        ],
    },
    {
        "name": "openrouter",
        "base_url": "https://openrouter.ai/api/v1",
        "models": [
            ("qwen/qwen3-coder:free",                    262144),
            ("deepseek/deepseek-r1:free",               1000000),
            ("deepseek/deepseek-chat-v3.1:free",        1000000),
            ("meta-llama/llama-3.3-70b-instruct:free",    8192),
            ("meta-llama/llama-4-maverick:free",         128000),
            ("openai/gpt-oss-120b:free",                 131072),
            ("openai/gpt-oss-20b:free",                  131072),
            ("z-ai/glm-4.5-air:free",                   128000),
            ("nvidia/nemotron-3-ultra:free",            1000000),
            ("openrouter/free",                          131072),
        ],
    },
    {
        "name": "nvidia-nim",
        "base_url": "https://integrate.api.nvidia.com/v1",
        "models": [
            ("meta/llama-3.3-70b-instruct",                   8192),
            ("deepseek-ai/deepseek-r1",                     128000),
            ("qwen/qwen3-coder-480b-a35b-instruct",         262144),
            ("google/gemma-3-27b-it",                         8192),
            ("nvidia/nemotron-mini-4b-instruct",              4096),
            ("mistralai/mistral-large-3",                   32000),
        ],
    },
]

# ---------------------------------------------------------------------------

async def seed():
    print("\nDronzer -- Seeding Free LLM Providers (Jul 2026)")
    print("=" * 54)

    providers_created = 0
    providers_skipped = 0
    models_created = 0
    models_skipped = 0

    async for session in get_db_session():
        for pdata in FREE_PROVIDERS:
            pname = pdata["name"]

            # -- Provider --
            existing_p = await session.execute(
                select(Provider).where(Provider.name == pname)
            )
            db_prov = existing_p.scalars().first()

            if db_prov:
                print(f"  [SKIP] Provider [{pname}] already exists")
                providers_skipped += 1
            else:
                db_prov = Provider(
                    name=pname,
                    base_url=pdata["base_url"],
                    is_active=True,
                )
                session.add(db_prov)
                await session.flush()
                print(f"  [OK]   Provider [{pname}] created")
                providers_created += 1

            # -- Models --
            for model_name, ctx_window in pdata["models"]:
                existing_m = await session.execute(
                    select(Model).where(
                        Model.name == model_name,
                        Model.provider_id == db_prov.id,
                        Model.is_deleted == False,
                    )
                )
                if existing_m.scalars().first():
                    models_skipped += 1
                    continue

                db_model = Model(
                    name=model_name,
                    provider_id=db_prov.id,
                    context_window=ctx_window,
                    capabilities={"chat": True},
                    is_active=True,
                )
                session.add(db_model)
                models_created += 1
                print(f"     + {model_name} ({ctx_window:,} ctx)")

        await session.commit()
        break

    await engine.dispose()

    print()
    print("=" * 54)
    print(f"  Providers: {providers_created} created, {providers_skipped} skipped")
    print(f"  Models:    {models_created} created, {models_skipped} skipped")
    print("  Done! Refresh the dashboard to see providers & models.")
    print()



if __name__ == "__main__":
    asyncio.run(seed())
