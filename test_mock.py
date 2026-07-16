from unittest.mock import patch, MagicMock, AsyncMock
import asyncio

async def run():
    mock_factory = MagicMock()
    mock_session = AsyncMock()
    mock_factory.return_value.__aenter__.return_value = mock_session
    
    try:
        async with mock_factory() as session:
            print("Session:", session)
    except Exception as e:
        print("Error:", type(e), e)

asyncio.run(run())
