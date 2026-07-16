import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { organizationsApi } from "@/lib/api/organizations";
import type { OrganizationCreate } from "@/lib/api/types";
import { toast } from "sonner";

export function useOrganizations() {
  return useQuery({
    queryKey: ["organizations"],
    queryFn: () => organizationsApi.list(),
  });
}

export function useOrganization(orgId: string) {
  return useQuery({
    queryKey: ["organizations", orgId],
    queryFn: () => organizationsApi.get(orgId),
    enabled: !!orgId,
  });
}

export function useCreateOrg() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: OrganizationCreate) => organizationsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["organizations"] });
      toast.success("Organization created successfully");
    },
    onError: (err: Error) => {
      toast.error(err.message || "Failed to create organization");
    },
  });
}

export function useDeleteOrg() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (orgId: string) => organizationsApi.remove(orgId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["organizations"] });
      toast.success("Organization deleted");
    },
    onError: (err: Error) => {
      toast.error(err.message || "Failed to delete organization");
    },
  });
}
