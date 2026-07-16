import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { healthApi } from "@/lib/api/health";

export function useHealthMetrics() {
  return useQuery({
    queryKey: ["health", "metrics"],
    queryFn: () => healthApi.getMetrics(),
    refetchInterval: 30_000, // auto-refresh every 30s
  });
}

export function useHealthDiagnostics() {
  return useQuery({
    queryKey: ["health", "diagnostics"],
    queryFn: () => healthApi.getDiagnostics(),
    refetchInterval: 30_000,
  });
}

export function useLiveness() {
  return useQuery({
    queryKey: ["health", "liveness"],
    queryFn: () => healthApi.getLiveness(),
    refetchInterval: 15_000, // more frequent for liveness
  });
}

export function useReadiness() {
  return useQuery({
    queryKey: ["health", "readiness"],
    queryFn: () => healthApi.getReadiness(),
    refetchInterval: 15_000,
  });
}
