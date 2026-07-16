import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { pluginsApi } from "@/lib/api/plugins";
import { toast } from "sonner";

export function usePlugins() {
  return useQuery({
    queryKey: ["plugins"],
    queryFn: () => pluginsApi.list(),
  });
}

export function useReloadPlugins() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => pluginsApi.reload(),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["plugins"] });
      toast.success(data.message || "Plugins reloaded");
    },
    onError: (err: Error) => {
      toast.error(err.message || "Failed to reload plugins");
    },
  });
}
