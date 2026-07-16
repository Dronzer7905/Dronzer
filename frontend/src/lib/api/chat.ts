import { gatewayApi, streamRequest } from "./client";
import type {
  ChatCompletionRequest,
  ChatCompletionResponse,
  ModelListResponse,
} from "./types";

export const chatApi = {
  /** POST /v1/chat/completions — non-streaming */
  complete: (data: ChatCompletionRequest) =>
    gatewayApi.post<ChatCompletionResponse>("/chat/completions", {
      ...data,
      stream: false,
    }),

  /**
   * POST /v1/chat/completions — streaming (SSE)
   * Returns a ReadableStream that emits SSE chunks.
   * Consumer is responsible for parsing `data: {...}` lines.
   */
  stream: (data: Omit<ChatCompletionRequest, "stream">, apiKey?: string, signal?: AbortSignal) =>
    streamRequest("/chat/completions", { ...data, stream: true }, { signal, apiKey }),

  /** GET /v1/models — list available gateway models */
  listModels: () =>
    gatewayApi.get<ModelListResponse>("/models"),
};
