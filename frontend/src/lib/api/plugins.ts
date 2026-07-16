import { adminApi } from "./client";
import type { PluginResponse, PluginReloadResponse } from "./types";

export const pluginsApi = {
  list: () =>
    adminApi.get<PluginResponse[]>("/plugins"),

  reload: () =>
    adminApi.post<PluginReloadResponse>("/plugins/reload"),
};
