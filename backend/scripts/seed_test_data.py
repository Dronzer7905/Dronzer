import asyncio
import uuid

from dronzer.infrastructure.database.core import engine, get_db_session
from dronzer.infrastructure.database.models.ai import APIKey, Model, Provider


async def seed():
    async for session in get_db_session():
        # Clean existing test data if any
        from sqlalchemy import text

        await session.execute(text("DELETE FROM gateway_keys;"))
        await session.execute(text("DELETE FROM api_keys;"))
        await session.execute(text("DELETE FROM models;"))
        await session.execute(text("DELETE FROM providers;"))
        await session.execute(text("DELETE FROM organizations;"))
        await session.flush()

        import hashlib

        from dronzer.infrastructure.database.models.gateway import GatewayKey
        from dronzer.infrastructure.database.models.tenant import Organization

        # Create an organization first
        org = Organization(name="Test Org", slug="test-org")
        session.add(org)
        await session.flush()

        # Add a dummy gateway key "sk-test-dronzer"
        hashed = hashlib.sha256(b"sk-test-dronzer").hexdigest()
        gk = GatewayKey(hashed_key=hashed, label="Test Gateway Key", organization_id=org.id)
        session.add(gk)

        # Create Groq Provider
        groq_provider = Provider(
            name="groq", base_url="https://api.groq.com/openai/v1", is_active=True
        )
        session.add(groq_provider)

        # Create Gemini Provider
        gemini_provider = Provider(
            name="gemini",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai",
            is_active=True,
        )
        session.add(gemini_provider)

        await session.flush()

        # 4. Insert Models
        print("Inserting Models...")
        models_data = [
            # Groq model
            {
                "id": uuid.uuid4(),
                "provider_id": groq_provider.id,
                "name": "llama-3.1-8b-instant",
                "context_window": 8192,
                "capabilities": {"chat": True, "vision": False, "json_mode": True},
                "is_active": True,
            },
            # Gemini model
            {
                "id": uuid.uuid4(),
                "provider_id": gemini_provider.id,
                "name": "gemini-3.5-flash",
                "context_window": 1048576,
                "capabilities": {"chat": True, "vision": True, "json_mode": True},
                "is_active": True,
            },
        ]
        for m in models_data:
            session.add(Model(**m))

        await session.flush()

        # Add Keys
        groq_key = APIKey(
            provider_id=groq_provider.id,
            encrypted_key="gsk_PLACEHOLDER_KEY_FOR_TESTING",
            is_active=True,
            weight=10,
        )
        session.add(groq_key)

        # Add a second Groq key to test pooling/fallback
        groq_key_2 = APIKey(
            provider_id=groq_provider.id,
            encrypted_key="gsk_FAKE_GROQ_KEY_FOR_TESTING_POOLING_FALLBACK",
            is_active=True,
            weight=5,
        )
        session.add(groq_key_2)

        gemini_key = APIKey(
            provider_id=gemini_provider.id,
            encrypted_key="AQ.FAKE_KEY_FOR_TESTING_REMOVED_SECRET",
            is_active=True,
        )
        session.add(gemini_key)

        await session.commit()
        print("Test data seeded successfully!")
        break
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
