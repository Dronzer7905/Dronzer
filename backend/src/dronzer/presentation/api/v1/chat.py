import json

import structlog
from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from dronzer.application.orchestration.pipeline import RequestPipeline
from dronzer.infrastructure.database.core import get_db_session
from dronzer.presentation.schemas.openai import ChatCompletionRequest, ChatCompletionResponse

# In a real DI setup, we'd inject this via Depends.
# We'll assume the pipeline is stored on app.state for Phase 14 foundation.

logger = structlog.get_logger("dronzer.api.v1.chat")
router = APIRouter(prefix="/chat", tags=["Chat"])

import uuid


async def _stream_generator(
    pipeline: RequestPipeline,
    payload: dict,
    tenant_id: uuid.UUID,
    session: AsyncSession,
    request_state: dict,
):
    """Translates the pipeline's async generator into SSE format for FastAPI StreamingResponse."""
    try:
        generator = await pipeline.process_request(tenant_id, payload, session, request_state)
        async for chunk in generator:
            # Format as SSE
            data = json.dumps(chunk)
            yield f"data: {data}\n\n"
        yield "data: [DONE]\n\n"
    except Exception as e:
        logger.error("Streaming error", error=str(e), exc_info=True)
        error_chunk = {
            "error": {"message": "An error occurred during streaming.", "type": "server_error"}
        }
        yield f"data: {json.dumps(error_chunk)}\n\n"
        yield "data: [DONE]\n\n"


@router.post("/completions", response_model=ChatCompletionResponse)
async def chat_completions(
    request: Request,
    body: ChatCompletionRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_db_session),
):
    """
    OpenAI-compatible /v1/chat/completions endpoint.
    Routes the request through the Dronzer Orchestration Engine.
    """
    # Grab the pipeline from app state (injected during startup)
    pipeline: RequestPipeline = request.app.state.pipeline
    getattr(request.state, "api_key", "")

    # Convert Pydantic model back to dict for the pipeline
    payload = body.model_dump(exclude_unset=True)

    # Extract validated tenant UUID from request state
    if not hasattr(request.state, "organization_id") or not request.state.organization_id:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=401, detail="Unauthorized: No valid organization attached to this key."
        )

    tenant_id = request.state.organization_id

    if body.stream:
        # Return SSE Stream
        return StreamingResponse(
            _stream_generator(pipeline, payload, tenant_id, session, request.state.__dict__),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
        )
    else:
        # Standard synchronous execution
        result = await pipeline.process_request(tenant_id, payload, session, request.state.__dict__)
        return result
