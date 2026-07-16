import { adminApi } from "./client";
import type { ProjectCreate, ProjectResponse } from "./types";

export const projectsApi = {
  list: (orgId?: string) =>
    adminApi.get<ProjectResponse[]>("/projects", {
      params: orgId ? { org_id: orgId } : undefined,
    }),

  get: (projectId: string) =>
    adminApi.get<ProjectResponse>(`/projects/${projectId}`),

  create: (data: ProjectCreate) =>
    adminApi.post<ProjectResponse>("/projects", data),

  remove: (projectId: string) =>
    adminApi.delete<{ status: string }>(`/projects/${projectId}`),
};
