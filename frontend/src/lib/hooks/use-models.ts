import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { modelsApi } from "@/lib/api/models";
import type { ModelConfigResponse, ModelUpdateParams, ModelCreate } from "@/lib/api/types";
import { toast } from "sonner";

export function useModels(providerId?: string) {
  return useQuery({
    queryKey: ["models", providerId],
    queryFn: () => modelsApi.list(providerId),
  });
}

export function useUpdateModel() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ modelId, params }: { modelId: string; params: ModelUpdateParams }) =>
      modelsApi.update(modelId, params),
    onMutate: async ({ modelId, params }) => {
      // Optimistic update for toggle
      await queryClient.cancelQueries({ queryKey: ["models"] });
      const previous = queryClient.getQueryData<ModelConfigResponse[]>(["models", undefined]);
      if (params.is_enabled !== undefined) {
        queryClient.setQueryData<ModelConfigResponse[]>(["models", undefined], (old) =>
          old?.map((m) => (m.id === modelId ? { ...m, is_enabled: params.is_enabled! } : m))
        );
      }
      return { previous };
    },
    onError: (err: Error, _vars, context) => {
      if (context?.previous) {
        queryClient.setQueryData(["models", undefined], context.previous);
      }
      toast.error(err.message || "Failed to update model");
    },
    onSuccess: () => {
      toast.success("Model updated");
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["models"] });
    },
  });
}

export function useCreateModel() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: ModelCreate) => modelsApi.create(data),
    onSuccess: () => {
      toast.success("Model added successfully");
      queryClient.invalidateQueries({ queryKey: ["models"] });
    },
    onError: (err: Error) => {
      toast.error(err.message || "Failed to add model");
    },
  });
}
