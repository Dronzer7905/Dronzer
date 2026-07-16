import { adminApi } from "./client";
import type { ModelConfigResponse, ModelUpdateParams, ModelCreate } from "./types";

export const modelsApi = {
  list: (providerId?: string) =>
    adminApi.get<ModelConfigResponse[]>("/models", {
      params: providerId ? { provider_id: providerId } : undefined,
    }),

  create: (data: ModelCreate) =>
    adminApi.post<ModelConfigResponse>("/models", data),


  update: (modelId: string, params: ModelUpdateParams) =>
    adminApi.patch<ModelConfigResponse>(`/models/${modelId}`, undefined, {
      params: {
        ...(params.is_enabled !== undefined && { is_enabled: params.is_enabled }),
        ...(params.context_window !== undefined && { context_window: params.context_window }),
      },
    }),
};
