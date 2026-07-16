import { adminApi } from "./client";
import type { LoginRequest, TokenResponse, RefreshRequest, SetupRequest, SetupStatusResponse } from "./types";

export const authApi = {
  getSetupStatus: () =>
    adminApi.get<SetupStatusResponse>("/auth/setup-status", { noAuth: true }),

  setup: (data: SetupRequest) =>
    adminApi.post<TokenResponse>("/auth/setup", data, { noAuth: true }),

  login: (data: LoginRequest) =>
    adminApi.post<TokenResponse>("/auth/login", data, { noAuth: true }),

  refresh: (data: RefreshRequest) =>
    adminApi.post<TokenResponse>("/auth/refresh", data, { noAuth: true }),
};
