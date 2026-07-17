// ============================================================
// Dronzer AI Gateway — Centralized API Client
// Uses native fetch. Reads base URLs from environment variables
// so they are swappable per deployment (never hardcode localhost).
// ============================================================

import type { ApiError, SimpleError } from "./types";

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

const ADMIN_BASE = process.env.NEXT_PUBLIC_ADMIN_API_URL ?? "/admin";
const GATEWAY_BASE = process.env.NEXT_PUBLIC_GATEWAY_API_URL ?? "/v1";
const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "";

// ---------------------------------------------------------------------------
// Token helpers — read from Zustand persisted localStorage
// NOTE: We store tokens in localStorage because the backend returns them in
// the response body (not as httpOnly cookies). This is an XSS tradeoff:
// a more secure setup would use httpOnly cookies set by a BFF / Next.js
// route handler, but the current backend does not support that flow.
// ---------------------------------------------------------------------------

function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem("auth-storage");
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    return parsed?.state?.accessToken ?? null;
  } catch {
    return null;
  }
}

function clearSession() {
  if (typeof window === "undefined") return;
  localStorage.removeItem("auth-storage");
  localStorage.removeItem("app-storage");
  window.location.href = "/login";
}

// ---------------------------------------------------------------------------
// Error parsing
// ---------------------------------------------------------------------------

export class DronzerApiError extends Error {
  public status: number;
  public code?: string;
  public type?: string;
  public param?: string;

  constructor(
    message: string,
    status: number,
    opts?: { code?: string; type?: string; param?: string }
  ) {
    super(message);
    this.name = "DronzerApiError";
    this.status = status;
    this.code = opts?.code;
    this.type = opts?.type;
    this.param = opts?.param;
  }
}

async function parseErrorResponse(res: Response): Promise<DronzerApiError> {
  try {
    const body = await res.json();

    // OpenAI-compatible format: { error: { message, type, code, param } }
    if (body?.error?.message) {
      const err = body as ApiError;
      return new DronzerApiError(err.error.message, res.status, {
        code: err.error.code ?? undefined,
        type: err.error.type,
        param: err.error.param ?? undefined,
      });
    }

    // Simple format: { detail: "..." }
    if (body?.detail) {
      const err = body as SimpleError;
      return new DronzerApiError(err.detail, res.status);
    }

    return new DronzerApiError(JSON.stringify(body), res.status);
  } catch {
    return new DronzerApiError(res.statusText || "Request failed", res.status);
  }
}

// ---------------------------------------------------------------------------
// Core fetch wrapper
// ---------------------------------------------------------------------------

type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

interface RequestOptions {
  /** Skip automatic auth header (for public endpoints like login) */
  noAuth?: boolean;
  /** Query parameters */
  params?: Record<string, string | number | boolean | undefined>;
  /** AbortSignal for cancellation */
  signal?: AbortSignal;
}

async function request<T>(
  base: string,
  method: HttpMethod,
  path: string,
  body?: unknown,
  opts?: RequestOptions
): Promise<T> {
  // Ensure base doesn't end with slash and path doesn't start with slash
  const cleanBase = base.endsWith("/") ? base.slice(0, -1) : base;
  const cleanPath = path.startsWith("/") ? path.slice(1) : path;
  const urlStr = cleanBase ? `${cleanBase}/${cleanPath}` : `/${cleanPath}`;

  const fallbackBase = typeof window === "undefined" ? "http://127.0.0.1:8000" : window.location.origin;
  const url = urlStr.startsWith("/") 
    ? new URL(urlStr, fallbackBase)
    : new URL(urlStr);

  // Append query params
  if (opts?.params) {
    Object.entries(opts.params).forEach(([key, val]) => {
      if (val !== undefined && val !== null) {
        url.searchParams.set(key, String(val));
      }
    });
  }

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (!opts?.noAuth) {
    const token = getAccessToken();
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
  }

  const res = await fetch(url.toString(), {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
    signal: opts?.signal,
  });

  // 401 → clear session and redirect (except on login route)
  if (res.status === 401 && !opts?.noAuth) {
    clearSession();
    throw new DronzerApiError("Session expired", 401);
  }

  if (!res.ok) {
    throw await parseErrorResponse(res);
  }

  // Some endpoints return 204 No Content
  if (res.status === 204) return undefined as T;

  return res.json() as Promise<T>;
}

// ---------------------------------------------------------------------------
// Streaming fetch (for SSE chat completions)
// ---------------------------------------------------------------------------

export async function streamRequest(
  path: string,
  body: unknown,
  opts?: { signal?: AbortSignal; apiKey?: string }
): Promise<ReadableStream<Uint8Array>> {
  const cleanBase = GATEWAY_BASE.endsWith("/") ? GATEWAY_BASE.slice(0, -1) : GATEWAY_BASE;
  const cleanPath = path.startsWith("/") ? path.slice(1) : path;
  const urlStr = cleanBase ? `${cleanBase}/${cleanPath}` : `/${cleanPath}`;

  const fallbackBase = typeof window === "undefined" ? "http://127.0.0.1:8000" : window.location.origin;
  const url = urlStr.startsWith("/") 
    ? new URL(urlStr, fallbackBase)
    : new URL(urlStr);

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (opts?.apiKey) {
    headers["Authorization"] = `Bearer ${opts.apiKey}`;
  } else {
    const token = getAccessToken();
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
  }

  const res = await fetch(url.toString(), {
    method: "POST",
    headers,
    body: JSON.stringify(body),
    signal: opts?.signal,
  });

  if (!res.ok) {
    throw await parseErrorResponse(res);
  }

  if (!res.body) {
    throw new DronzerApiError("No response body for stream", 500);
  }

  return res.body;
}

// ---------------------------------------------------------------------------
// Public API — Admin endpoints
// ---------------------------------------------------------------------------

export const adminApi = {
  get: <T>(path: string, opts?: RequestOptions) =>
    request<T>(ADMIN_BASE, "GET", path, undefined, opts),

  post: <T>(path: string, body?: unknown, opts?: RequestOptions) =>
    request<T>(ADMIN_BASE, "POST", path, body, opts),

  patch: <T>(path: string, body?: unknown, opts?: RequestOptions) =>
    request<T>(ADMIN_BASE, "PATCH", path, body, opts),

  delete: <T>(path: string, opts?: RequestOptions) =>
    request<T>(ADMIN_BASE, "DELETE", path, undefined, opts),
};

// ---------------------------------------------------------------------------
// Public API — Gateway endpoints (OpenAI-compatible)
// ---------------------------------------------------------------------------

export const gatewayApi = {
  get: <T>(path: string, opts?: RequestOptions) =>
    request<T>(GATEWAY_BASE, "GET", path, undefined, opts),

  post: <T>(path: string, body?: unknown, opts?: RequestOptions) =>
    request<T>(GATEWAY_BASE, "POST", path, body, opts),
};

// ---------------------------------------------------------------------------
// Public API — Base URL endpoints (health probes)
// ---------------------------------------------------------------------------

export const baseApi = {
  get: <T>(path: string, opts?: RequestOptions) =>
    request<T>(BASE_URL, "GET", path, undefined, opts),
};
