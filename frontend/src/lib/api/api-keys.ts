import { adminApi } from "./client";
import type { APIKeyCreate, APIKeyResponse } from "./types";

export const apiKeysApi = {
  list: (filters?: { project_id?: string; provider_id?: string }) =>
    adminApi.get<APIKeyResponse[]>("/keys", {
      params: filters,
    }),

  create: (data: APIKeyCreate) =>
    adminApi.post<APIKeyResponse>("/keys", data),

  revoke: (keyId: string) =>
    adminApi.delete<{ status: string }>(`/keys/${keyId}`),
};
