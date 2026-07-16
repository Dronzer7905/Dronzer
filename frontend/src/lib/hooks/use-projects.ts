import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { projectsApi } from "@/lib/api/projects";
import type { ProjectCreate } from "@/lib/api/types";
import { toast } from "sonner";

export function useProjects(orgId?: string) {
  return useQuery({
    queryKey: ["projects", orgId],
    queryFn: () => projectsApi.list(orgId),
    enabled: !!orgId,
  });
}

export function useCreateProject() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: ProjectCreate) => projectsApi.create(data),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: ["projects", variables.org_id] });
      toast.success("Project created successfully");
    },
    onError: (err: Error) => {
      toast.error(err.message || "Failed to create project");
    },
  });
}

export function useDeleteProject() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (projectId: string) => projectsApi.remove(projectId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["projects"] });
      toast.success("Project deleted");
    },
    onError: (err: Error) => {
      toast.error(err.message || "Failed to delete project");
    },
  });
}
