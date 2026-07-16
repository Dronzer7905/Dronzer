import { adminApi } from "./client";
import type { GatewayKeyCreate, GatewayKeyResponse } from "./types";

export const gatewayKeysApi = {
  list: (params?: { organization_id?: string }) => 
    adminApi.get<GatewayKeyResponse[]>("/gateway-keys", { params }),

  create: (data: GatewayKeyCreate) =>
    adminApi.post<GatewayKeyResponse>("/gateway-keys", data),

  revoke: (keyId: string) =>
    adminApi.delete<{status: string}>(`/gateway-keys/${keyId}`),
};
