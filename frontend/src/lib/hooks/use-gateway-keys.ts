import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { gatewayKeysApi } from "@/lib/api/gateway-keys";
import type { GatewayKeyCreate } from "@/lib/api/types";
import { toast } from "sonner";

export function useGatewayKeys(filters?: { organization_id?: string }) {
  return useQuery({
    queryKey: ["gateway-keys", filters],
    queryFn: () => gatewayKeysApi.list(filters),
    enabled: !!filters?.organization_id, // Wait for org_id to be available
  });
}

export function useCreateGatewayKey() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: GatewayKeyCreate) => gatewayKeysApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["gateway-keys"] });
      toast.success("Gateway API key created");
    },
    onError: (err: Error) => {
      toast.error(err.message || "Failed to create Gateway API key");
    },
  });
}

export function useRevokeGatewayKey() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (keyId: string) => gatewayKeysApi.revoke(keyId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["gateway-keys"] });
      toast.success("Gateway API key revoked");
    },
    onError: (err: Error) => {
      toast.error(err.message || "Failed to revoke Gateway API key");
    },
  });
}
