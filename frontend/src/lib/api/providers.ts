import { adminApi } from "./client";
import type { ProviderConfigResponse, ProviderToggleResponse, ProviderCreate } from "./types";

export const providersApi = {
  list: () =>
    adminApi.get<ProviderConfigResponse[]>("/providers"),

  create: (data: ProviderCreate) =>
    adminApi.post<ProviderConfigResponse>("/providers", data),

  enable: (providerId: string) =>
    adminApi.post<ProviderToggleResponse>(`/providers/${providerId}/enable`),

  disable: (providerId: string) =>
    adminApi.post<ProviderToggleResponse>(`/providers/${providerId}/disable`),
};
