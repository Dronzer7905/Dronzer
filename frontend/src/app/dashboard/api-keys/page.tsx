"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { motion } from "framer-motion";
import * as Dialog from "@radix-ui/react-dialog";
import { Key, Plus, Trash2, Search, Loader2, X, AlertCircle, Eye, EyeOff } from "lucide-react";
import Link from "next/link";

import { useApiKeys, useCreateApiKey, useRevokeApiKey } from "@/lib/hooks/use-api-keys";
import { useProviders } from "@/lib/hooks/use-providers";
import { useProjects } from "@/lib/hooks/use-projects";
import { useAppStore } from "@/lib/stores/app-store";
import { StatusPill } from "@/components/ui/status-pill";
import { EmptyState } from "@/components/ui/empty-state";
import { ConfirmationModal } from "@/components/ui/confirmation-modal";
import { SkeletonTable } from "@/components/ui/skeleton";
import type { APIKeyResponse } from "@/lib/api/types";
import { cn } from "@/lib/utils";

const keySchema = z.object({
  label: z.string().min(1, "Label is required"),
  provider_id: z.string().min(1, "Select a provider"),
  project_id: z.string().min(1, "Select a project"),
  key_value: z.string().min(1, "API key value is required"),
});
type KeyForm = z.infer<typeof keySchema>;

export default function ApiKeysPage() {
  const { activeOrganization } = useAppStore();
  const { data: keys, isLoading } = useApiKeys();
  const { data: providers } = useProviders();
  const { data: projects } = useProjects(activeOrganization?.id);
  
  const createKey = useCreateApiKey();
  const revokeKey = useRevokeApiKey();

  const [search, setSearch] = useState("");
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [keyToRevoke, setKeyToRevoke] = useState<APIKeyResponse | null>(null);
  const [showKeyVal, setShowKeyVal] = useState(false);

  const { register, handleSubmit, reset, formState: { errors } } = useForm<KeyForm>({
    resolver: zodResolver(keySchema),
    defaultValues: { label: "", provider_id: "", project_id: "", key_value: "" }
  });

  const filteredKeys = keys?.filter(k => 
    k.label?.toLowerCase().includes(search.toLowerCase()) || 
    k.provider_id.toLowerCase().includes(search.toLowerCase())
  ) || [];

  const handleCreate = async (data: KeyForm) => {
    try {
      await createKey.mutateAsync(data);
      setIsCreateOpen(false);
      reset();
      setShowKeyVal(false);
    } catch (e) {
      // handled by mutation
    }
  };

  const handleRevoke = async () => {
    if (!keyToRevoke) return;
    try {
      await revokeKey.mutateAsync(keyToRevoke.id);
    } catch (e) {
      // handled by mutation
    }
  };

  const getProviderName = (id: string) => providers?.find(p => p.id === id)?.name || id;
  const getProjectName = (id: string) => projects?.find(p => p.id === id)?.name || id;

  if (!activeOrganization) {
    return (
      <div className="max-w-3xl mx-auto mt-12">
        <div className="glass-card p-8 flex flex-col items-center text-center">
          <div className="w-16 h-16 rounded-full bg-warning-muted flex items-center justify-center mb-4">
            <AlertCircle className="w-8 h-8 text-warning" />
          </div>
          <h2 className="text-xl font-bold text-text-primary mb-2">No Organization Selected</h2>
          <p className="text-text-secondary mb-6 max-w-md">
            You need to select an active organization to manage API keys.
          </p>
          <Link href="/dashboard/organizations" className="px-5 py-2.5 rounded-lg gradient-accent text-white font-medium">
            Go to Organizations
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row gap-4 sm:items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-text-primary tracking-tight">Provider Credentials</h2>
          <p className="text-sm text-text-secondary mt-1">Manage provider authentication credentials.</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-tertiary" />
            <input 
              type="text" 
              placeholder="Search keys..." 
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="input-field pl-9 h-10 w-full sm:w-64"
            />
          </div>
          <button 
            onClick={() => setIsCreateOpen(true)}
            className="h-10 px-4 rounded-lg gradient-accent text-white text-sm font-medium flex items-center gap-2 hover:opacity-90 transition-opacity"
          >
            <Plus className="w-4 h-4" />
            <span className="hidden sm:inline">Add API Key</span>
          </button>
        </div>
      </div>

      {/* Table */}
      {isLoading ? (
        <div className="glass-card overflow-hidden">
          <SkeletonTable rows={5} />
        </div>
      ) : filteredKeys.length === 0 ? (
        <EmptyState 
          icon={Key}
          title={search ? "No keys found" : "No API keys yet"}
          description={search ? `No results for "${search}"` : "Add a provider API key to start routing requests."}
          action={
            !search && (
              <button 
                onClick={() => setIsCreateOpen(true)}
                className="px-4 py-2 rounded-lg gradient-accent text-white text-sm font-medium"
              >
                Add API Key
              </button>
            )
          }
        />
      ) : (
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card overflow-hidden"
        >
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-bg-elevated border-b border-border-primary text-text-secondary">
                <tr>
                  <th className="px-6 py-3 font-medium">Label</th>
                  <th className="px-6 py-3 font-medium">Provider</th>
                  <th className="px-6 py-3 font-medium">Project</th>
                  <th className="px-6 py-3 font-medium">Status</th>
                  <th className="px-6 py-3 font-medium text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border-primary">
                {filteredKeys.map((key) => {
                  let status: 'active' | 'failing' | 'inactive' = 'inactive';
                  if (key.is_active && !key.is_failing) status = 'active';
                  else if (key.is_failing) status = 'failing';

                  return (
                    <tr key={key.id} className="hover:bg-bg-card-hover transition-colors group">
                      <td className="px-6 py-4 font-medium text-text-primary">
                        {key.label || <span className="text-text-muted italic">Unnamed Key</span>}
                      </td>
                      <td className="px-6 py-4">
                        <span className="inline-flex items-center px-2 py-1 rounded bg-bg-elevated border border-border-primary text-xs font-mono text-text-secondary">
                          {getProviderName(key.provider_id)}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-text-secondary">
                        {getProjectName(key.project_id)}
                      </td>
                      <td className="px-6 py-4">
                        <StatusPill status={status} />
                      </td>
                      <td className="px-6 py-4 text-right">
                        <button
                          onClick={() => setKeyToRevoke(key)}
                          className="p-2 text-text-tertiary hover:text-error hover:bg-error-muted rounded-lg transition-colors inline-flex opacity-0 group-hover:opacity-100 focus:opacity-100 focus:outline-none"
                          title="Revoke Key"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </motion.div>
      )}

      {/* Create Modal */}
      <Dialog.Root open={isCreateOpen} onOpenChange={setIsCreateOpen}>
        <Dialog.Portal>
          <Dialog.Overlay className="fixed inset-0 bg-bg-overlay backdrop-blur-sm z-50 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />
          <Dialog.Content className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-md glass-card p-6 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95">
            <div className="flex items-center justify-between mb-6">
              <Dialog.Title className="text-lg font-semibold text-text-primary">Add API Key</Dialog.Title>
              <Dialog.Close asChild>
                <button className="p-1 rounded-lg hover:bg-bg-elevated text-text-tertiary hover:text-text-primary transition-colors">
                  <X className="w-4 h-4" />
                </button>
              </Dialog.Close>
            </div>
            
            <form onSubmit={handleSubmit(handleCreate)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1.5">Label</label>
                <input 
                  {...register("label")} 
                  autoFocus
                  className="input-field w-full h-10" 
                  placeholder="e.g. OpenAI Prod Key"
                  disabled={createKey.isPending}
                />
                {errors.label && <p className="mt-1.5 text-xs text-error">{errors.label.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1.5">Provider</label>
                <select 
                  {...register("provider_id")} 
                  className="input-field w-full h-10 appearance-none bg-[url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20width%3D%2224%22%20height%3D%2224%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cpath%20d%3D%22M7%2010l5%205%205-5z%22%20fill%3D%22%236b7280%22%2F%3E%3C%2Fsvg%3E')] bg-[length:24px_24px] bg-[right_8px_center] bg-no-repeat"
                  disabled={createKey.isPending || !providers}
                >
                  <option value="">Select a provider...</option>
                  {providers?.map(p => (
                    <option key={p.id} value={p.id}>{p.name}</option>
                  ))}
                </select>
                {errors.provider_id && <p className="mt-1.5 text-xs text-error">{errors.provider_id.message}</p>}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1.5">Project</label>
                <select 
                  {...register("project_id")} 
                  className="input-field w-full h-10 appearance-none bg-[url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20width%3D%2224%22%20height%3D%2224%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cpath%20d%3D%22M7%2010l5%205%205-5z%22%20fill%3D%22%236b7280%22%2F%3E%3C%2Fsvg%3E')] bg-[length:24px_24px] bg-[right_8px_center] bg-no-repeat"
                  disabled={createKey.isPending || !projects}
                >
                  <option value="">Select a project...</option>
                  {projects?.map(p => (
                    <option key={p.id} value={p.id}>{p.name}</option>
                  ))}
                </select>
                {errors.project_id && <p className="mt-1.5 text-xs text-error">{errors.project_id.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1.5">Key Value</label>
                <div className="relative">
                  <input 
                    {...register("key_value")} 
                    type={showKeyVal ? "text" : "password"}
                    className="input-field w-full h-10 pr-10 font-mono text-sm" 
                    placeholder="sk-..."
                    disabled={createKey.isPending}
                  />
                  <button
                    type="button"
                    onClick={() => setShowKeyVal(!showKeyVal)}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center text-text-tertiary hover:text-text-primary"
                  >
                    {showKeyVal ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
                {errors.key_value && <p className="mt-1.5 text-xs text-error">{errors.key_value.message}</p>}
              </div>
              
              <div className="pt-4 flex justify-end gap-3">
                <Dialog.Close asChild>
                  <button type="button" className="px-4 py-2 rounded-lg text-sm font-medium bg-bg-elevated border border-border-primary text-text-secondary hover:text-text-primary">
                    Cancel
                  </button>
                </Dialog.Close>
                <button 
                  type="submit" 
                  disabled={createKey.isPending}
                  className="px-4 py-2 rounded-lg text-sm font-medium text-white gradient-accent hover:opacity-90 flex items-center gap-2 disabled:opacity-70"
                >
                  {createKey.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
                  Add Key
                </button>
              </div>
            </form>
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>

      {/* Delete Confirmation */}
      <ConfirmationModal
        open={!!keyToRevoke}
        onOpenChange={(open) => !open && setKeyToRevoke(null)}
        title="Revoke API Key"
        description={`Are you sure you want to revoke the key "${keyToRevoke?.label}"? This action cannot be undone and any applications using it will immediately lose access.`}
        variant="danger"
        confirmLabel="Revoke Key"
        onConfirm={handleRevoke}
        loading={revokeKey.isPending}
      />
    </div>
  );
}
