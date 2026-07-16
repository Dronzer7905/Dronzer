from typing import Any, Literal

from pydantic import BaseModel, Field

# ---------------------------------------------------------
# Chat Completions Request Schemas
# ---------------------------------------------------------


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant", "function", "tool"]
    content: str | list[dict[str, Any]]
    name: str | None = None
    tool_calls: list[dict[str, Any]] | None = None
    tool_call_id: str | None = None


class ResponseFormat(BaseModel):
    type: Literal["text", "json_object"]


class ToolFunction(BaseModel):
    name: str
    description: str | None = None
    parameters: dict[str, Any] | None = None


class Tool(BaseModel):
    type: Literal["function"]
    function: ToolFunction


class ToolChoiceFunction(BaseModel):
    name: str


class ToolChoice(BaseModel):
    type: Literal["function"]
    function: ToolChoiceFunction


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    frequency_penalty: float | None = Field(default=0.0, ge=-2.0, le=2.0)
    logit_bias: dict[str, int] | None = None
    logprobs: bool | None = False
    top_logprobs: int | None = Field(default=None, ge=0, le=20)
    max_tokens: int | None = None
    n: int | None = Field(default=1, ge=1, le=128)
    presence_penalty: float | None = Field(default=0.0, ge=-2.0, le=2.0)
    response_format: ResponseFormat | None = None
    seed: int | None = None
    stop: str | list[str] | None = None
    stream: bool | None = False
    temperature: float | None = Field(default=1.0, ge=0.0, le=2.0)
    top_p: float | None = Field(default=1.0, ge=0.0, le=1.0)
    tools: list[Tool] | None = None
    tool_choice: Literal["none", "auto"] | ToolChoice | None = None
    user: str | None = None


# ---------------------------------------------------------
# Chat Completions Response Schemas
# ---------------------------------------------------------


class TokenUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionMessage(BaseModel):
    role: str
    content: str | None = None
    tool_calls: list[dict[str, Any]] | None = None


class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatCompletionMessage
    finish_reason: str | None = None
    logprobs: Any | None = None


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    system_fingerprint: str | None = None
    choices: list[ChatCompletionChoice]
    usage: TokenUsage | None = None


# ---------------------------------------------------------
# Models Schemas
# ---------------------------------------------------------


class ModelCard(BaseModel):
    id: str
    object: str = "model"
    created: int
    owned_by: str


class ModelListResponse(BaseModel):
    object: str = "list"
    data: list[ModelCard]


# ---------------------------------------------------------
# Embeddings Schemas
# ---------------------------------------------------------
class EmbeddingRequest(BaseModel):
    input: str | list[str]
    model: str
    encoding_format: str | None = "float"
    dimensions: int | None = None
    user: str | None = None


# ---------------------------------------------------------
# Images Schemas
# ---------------------------------------------------------
class ImageGenerationRequest(BaseModel):
    prompt: str
    model: str | None = "dall-e-3"
    n: int | None = 1
    quality: str | None = "standard"
    response_format: str | None = "url"
    size: str | None = "1024x1024"
    style: str | None = "vivid"
    user: str | None = None
