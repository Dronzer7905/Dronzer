import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiKeysApi } from "@/lib/api/api-keys";
import type { APIKeyCreate } from "@/lib/api/types";
import { toast } from "sonner";

export function useApiKeys(filters?: { project_id?: string; provider_id?: string }) {
  return useQuery({
    queryKey: ["api-keys", filters],
    queryFn: () => apiKeysApi.list(filters),
  });
}

export function useCreateApiKey() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: APIKeyCreate) => apiKeysApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["api-keys"] });
      toast.success("API key created");
    },
    onError: (err: Error) => {
      toast.error(err.message || "Failed to create API key");
    },
  });
}

export function useRevokeApiKey() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (keyId: string) => apiKeysApi.revoke(keyId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["api-keys"] });
      toast.success("API key revoked");
    },
    onError: (err: Error) => {
      toast.error(err.message || "Failed to revoke API key");
    },
  });
}
