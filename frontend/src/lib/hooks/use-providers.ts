import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { providersApi } from "@/lib/api/providers";
import type { ProviderConfigResponse, ProviderCreate } from "@/lib/api/types";
import { toast } from "sonner";

export function useProviders() {
  return useQuery({
    queryKey: ["providers"],
    queryFn: () => providersApi.list(),
  });
}

export function useToggleProvider() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ providerId, enable }: { providerId: string; enable: boolean }) =>
      enable ? providersApi.enable(providerId) : providersApi.disable(providerId),
    onMutate: async ({ providerId, enable }) => {
      // Optimistic update
      await queryClient.cancelQueries({ queryKey: ["providers"] });
      const previous = queryClient.getQueryData<ProviderConfigResponse[]>(["providers"]);
      queryClient.setQueryData<ProviderConfigResponse[]>(["providers"], (old) =>
        old?.map((p) => (p.id === providerId ? { ...p, is_enabled: enable } : p))
      );
      return { previous };
    },
    onError: (err: Error, _vars, context) => {
      // Revert optimistic update
      if (context?.previous) {
        queryClient.setQueryData(["providers"], context.previous);
      }
      toast.error(err.message || "Failed to update provider");
    },
    onSuccess: (_data, { enable }) => {
      toast.success(`Provider ${enable ? "enabled" : "disabled"}`);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["providers"] });
    },
  });
}

export function useCreateProvider() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: ProviderCreate) => providersApi.create(data),
    onSuccess: () => {
      toast.success("Provider added successfully");
      queryClient.invalidateQueries({ queryKey: ["providers"] });
    },
    onError: (err: Error) => {
      toast.error(err.message || "Failed to add provider");
    },
  });
}
