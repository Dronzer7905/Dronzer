import { adminApi } from "./client";
import type { OrganizationCreate, OrganizationResponse } from "./types";

export const organizationsApi = {
  list: () =>
    adminApi.get<OrganizationResponse[]>("/organizations"),

  get: (orgId: string) =>
    adminApi.get<OrganizationResponse>(`/organizations/${orgId}`),

  create: (data: OrganizationCreate) =>
    adminApi.post<OrganizationResponse>("/organizations", data),

  remove: (orgId: string) =>
    adminApi.delete<{ status: string }>(`/organizations/${orgId}`),
};
