// ============================================================
// App Store — Zustand + localStorage persistence
// Tracks active org/project context used to scope API calls.
// ============================================================

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { OrganizationResponse, ProjectResponse } from "@/lib/api/types";

interface AppState {
  activeOrganization: OrganizationResponse | null;
  activeProject: ProjectResponse | null;
  sidebarCollapsed: boolean;

  setActiveOrg: (org: OrganizationResponse | null) => void;
  setActiveProject: (project: ProjectResponse | null) => void;
  clearContext: () => void;
  toggleSidebar: () => void;
  setSidebarCollapsed: (collapsed: boolean) => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      activeOrganization: null,
      activeProject: null,
      sidebarCollapsed: false,

      setActiveOrg: (org) =>
        set({
          activeOrganization: org,
          // Clear project when org changes
          activeProject: null,
        }),

      setActiveProject: (project) =>
        set({ activeProject: project }),

      clearContext: () =>
        set({
          activeOrganization: null,
          activeProject: null,
        }),

      toggleSidebar: () =>
        set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),

      setSidebarCollapsed: (collapsed) =>
        set({ sidebarCollapsed: collapsed }),
    }),
    {
      name: "app-storage",
    }
  )
);
