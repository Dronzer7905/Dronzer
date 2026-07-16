import { adminApi, baseApi } from "./client";
import type {
  HealthMetrics,
  HealthDiagnostics,
  LivenessResponse,
  ReadinessResponse,
} from "./types";

export const healthApi = {
  /** GET /admin/health/metrics — requires auth */
  getMetrics: () =>
    adminApi.get<HealthMetrics>("/health/metrics"),

  /** GET /admin/health/diagnostics — requires auth */
  getDiagnostics: () =>
    adminApi.get<HealthDiagnostics>("/health/diagnostics"),

  /** GET /health/liveness — public probe */
  getLiveness: () =>
    baseApi.get<LivenessResponse>("/health/liveness", { noAuth: true }),

  /** GET /health/readiness — public probe */
  getReadiness: () =>
    baseApi.get<ReadinessResponse>("/health/readiness", { noAuth: true }),
};
