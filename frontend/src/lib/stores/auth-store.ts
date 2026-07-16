// ============================================================
// Auth Store — Zustand + localStorage persistence
// Manages JWT tokens, user email/role, and refresh logic.
// ============================================================

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { TokenPayload } from "@/lib/api/types";

interface AuthState {
  accessToken: string | null;
  refreshToken: string | null;
  userEmail: string | null;
  userRole: string | null;
  isAuthenticated: boolean;

  login: (accessToken: string, refreshToken: string) => void;
  logout: () => void;
  setTokens: (accessToken: string, refreshToken: string) => void;
}

/** Decode a JWT payload without verifying signature (client-side only). */
function decodeJwt(token: string): TokenPayload | null {
  try {
    const parts = token.split(".");
    if (parts.length !== 3) return null;
    const payload = JSON.parse(atob(parts[1]));
    return payload as TokenPayload;
  } catch {
    return null;
  }
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      accessToken: null,
      refreshToken: null,
      userEmail: null,
      userRole: null,
      isAuthenticated: false,

      login: (accessToken, refreshToken) => {
        const payload = decodeJwt(accessToken);
        set({
          accessToken,
          refreshToken,
          userEmail: payload?.sub ?? null,
          userRole: payload?.role ?? null,
          isAuthenticated: true,
        });
      },

      logout: () => {
        set({
          accessToken: null,
          refreshToken: null,
          userEmail: null,
          userRole: null,
          isAuthenticated: false,
        });
      },

      setTokens: (accessToken, refreshToken) => {
        const payload = decodeJwt(accessToken);
        set({
          accessToken,
          refreshToken,
          userEmail: payload?.sub ?? null,
          userRole: payload?.role ?? null,
          isAuthenticated: true,
        });
      },
    }),
    {
      name: "auth-storage",
    }
  )
);
