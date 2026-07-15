from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import os

# Import the official generated Dronzer Python SDK
from dronzer_client.client import DronzerClient

app = FastAPI(title="Dronzer SDK Example - Customer Support API")

# Initialize the SDK client singleton
# In production, DRONZER_API_KEY should be loaded securely from environment variables.
dronzer = DronzerClient(
    api_key=os.getenv("DRONZER_API_KEY", "dev_token_123"),
    base_url="https://api.dronzer.io/v1"
)

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import httpx

class SupportRequest(BaseModel):
    user_name: str
    subscription_tier: str
    user_query: str

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(httpx.RequestError)
)
async def fetch_llm_response(req: SupportRequest) -> str:
    """Helper function to execute prompt with exponential backoff on network failures."""
    return await dronzer.execute_prompt(
        prompt_id="support-bot-v2",
        variables={
            "user_name": req.user_name,
            "subscription_tier": req.subscription_tier,
            "user_query": req.user_query
        }
    )

@app.post("/api/support")
async def handle_support_query(req: SupportRequest):
    """
    Demonstrates integrating Dronzer PromptOps into a microservice.
    Instead of hardcoding Prompts and OpenAI calls here, we delegate to Dronzer.
    """
    try:
        response_text = await fetch_llm_response(req)
        return {"reply": response_text}
        
    except httpx.HTTPStatusError as e:
        # e.g., 429 Rate Limit Exceeded or 401 Unauthorized from Dronzer Gateway
        raise HTTPException(status_code=e.response.status_code, detail=f"Dronzer API Error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Service Error")

@app.on_event("shutdown")
async def shutdown_event():
    # Gracefully close the SDK connection pool
    await dronzer.close()
