"use client";

import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { motion } from "framer-motion";
import * as Dialog from "@radix-ui/react-dialog";
import { Key, Plus, Trash2, Search, Loader2, X, AlertCircle, Eye, EyeOff, Copy, ArrowUp, ArrowDown } from "lucide-react";
import Link from "next/link";
import { toast } from "sonner";

import { useGatewayKeys, useCreateGatewayKey, useRevokeGatewayKey } from "@/lib/hooks/use-gateway-keys";
import { useProjects } from "@/lib/hooks/use-projects";
import { useModels } from "@/lib/hooks/use-models";
import { useAppStore } from "@/lib/stores/app-store";
import { StatusPill } from "@/components/ui/status-pill";
import { EmptyState } from "@/components/ui/empty-state";
import { ConfirmationModal } from "@/components/ui/confirmation-modal";
import { SkeletonTable } from "@/components/ui/skeleton";
import type { GatewayKeyResponse } from "@/lib/api/types";

const keySchema = z.object({
  label: z.string().min(1, "Label is required"),
  project_id: z.string().optional(),
  task_type: z.string(),
});
type KeyForm = z.infer<typeof keySchema>;

export default function GatewayKeysPage() {
  const { activeOrganization } = useAppStore();
  const { data: keys, isLoading } = useGatewayKeys({ organization_id: activeOrganization?.id });
  const { data: projects } = useProjects(activeOrganization?.id);
  
  const createKey = useCreateGatewayKey();
  const revokeKey = useRevokeGatewayKey();

  const [search, setSearch] = useState("");
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [keyToRevoke, setKeyToRevoke] = useState<GatewayKeyResponse | null>(null);
  
  // State to hold a newly generated key so the user can copy it
  const [newlyCreatedKey, setNewlyCreatedKey] = useState<string | null>(null);

  const { register, handleSubmit, reset, watch, formState: { errors } } = useForm<KeyForm>({
    resolver: zodResolver(keySchema),
    defaultValues: { label: "", project_id: "", task_type: "chat" }
  });

  const { data: allModels } = useModels();
  const [modelPriorities, setModelPriorities] = useState<string[]>([]);
  const [hasUserEdited, setHasUserEdited] = useState(false);
  const watchTaskType = watch("task_type");

  useEffect(() => {
    if (allModels && watchTaskType && !hasUserEdited) {
      const capableModels = allModels.filter(m => m.capabilities?.[watchTaskType] === true);
      setModelPriorities(capableModels.map(m => m.id));
    }
  }, [watchTaskType, allModels, hasUserEdited]);

  const availableModels = allModels?.filter(m => !modelPriorities.includes(m.id)) || [];

  const handleAddModel = (e: React.ChangeEvent<HTMLSelectElement>) => {
    if (e.target.value) {
      setModelPriorities([...modelPriorities, e.target.value]);
      setHasUserEdited(true);
      e.target.value = "";
    }
  };

  const moveModelUp = (index: number) => {
    if (index === 0) return;
    const newPriorities = [...modelPriorities];
    [newPriorities[index - 1], newPriorities[index]] = [newPriorities[index], newPriorities[index - 1]];
    setModelPriorities(newPriorities);
    setHasUserEdited(true);
  };

  const moveModelDown = (index: number) => {
    if (index === modelPriorities.length - 1) return;
    const newPriorities = [...modelPriorities];
    [newPriorities[index + 1], newPriorities[index]] = [newPriorities[index], newPriorities[index + 1]];
    setModelPriorities(newPriorities);
    setHasUserEdited(true);
  };

  const removeModel = (index: number) => {
    setModelPriorities(modelPriorities.filter((_, i) => i !== index));
    setHasUserEdited(true);
  };

  const filteredKeys = keys?.filter(k => 
    k.label?.toLowerCase().includes(search.toLowerCase())
  ) || [];

  const handleCreate = async (data: KeyForm) => {
    if (!activeOrganization) return;
    try {
      const result = await createKey.mutateAsync({
        label: data.label,
        project_id: data.project_id || undefined,
        organization_id: activeOrganization.id,
        task_type: data.task_type,
        model_priorities: modelPriorities,
        provider_priorities: []
      });
      setNewlyCreatedKey(result.key_value || null);
      setIsCreateOpen(false);
      reset();
      setModelPriorities([]);
      setHasUserEdited(false);
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

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast.success("Copied to clipboard!");
  };

  const getProjectName = (id?: string | null) => {
    if (!id) return "All Projects (Org Level)";
    return projects?.find(p => p.id === id)?.name || id;
  };

  if (!activeOrganization) {
    return (
      <div className="max-w-3xl mx-auto mt-12">
        <div className="glass-card p-8 flex flex-col items-center text-center">
          <div className="w-16 h-16 rounded-full bg-warning-muted flex items-center justify-center mb-4">
            <AlertCircle className="w-8 h-8 text-warning" />
          </div>
          <h2 className="text-xl font-bold text-text-primary mb-2">No Organization Selected</h2>
          <p className="text-text-secondary mb-6 max-w-md">
            You need to select an active organization to manage Gateway Keys.
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
          <h2 className="text-2xl font-bold text-text-primary tracking-tight">Gateway Keys</h2>
          <p className="text-sm text-text-secondary mt-1">Generate API keys to authenticate your apps with Dronzer.</p>
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
            <span className="hidden sm:inline">Generate New Key</span>
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
          title={search ? "No keys found" : "No Gateway Keys yet"}
          description={search ? `No results for "${search}"` : "Generate a key to start sending requests to Dronzer."}
          action={
            !search && (
              <button 
                onClick={() => setIsCreateOpen(true)}
                className="px-4 py-2 rounded-lg gradient-accent text-white text-sm font-medium"
              >
                Generate Key
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
                  <th className="px-6 py-3 font-medium">Key Prefix</th>
                  <th className="px-6 py-3 font-medium">Project Access</th>
                  <th className="px-6 py-3 font-medium">Status</th>
                  <th className="px-6 py-3 font-medium">Created At</th>
                  <th className="px-6 py-3 font-medium text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border-primary">
                {filteredKeys.map((key) => {
                  const status = key.is_active ? 'active' : 'inactive';

                  return (
                    <tr key={key.id} className="hover:bg-bg-card-hover transition-colors group">
                      <td className="px-6 py-4 font-medium text-text-primary">
                        {key.label || <span className="text-text-muted italic">Unnamed Key</span>}
                      </td>
                      <td className="px-6 py-4">
                        <span className="font-mono text-text-secondary">
                          {key.key_value || "dz-sk-... (hidden)"}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-text-secondary">
                        {getProjectName(key.project_id)}
                      </td>
                      <td className="px-6 py-4">
                        <StatusPill status={status} />
                      </td>
                      <td className="px-6 py-4 text-text-tertiary">
                        {new Date(key.created_at).toLocaleDateString()}
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

      {/* Integration Guide */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="glass-card p-6 mt-8"
      >
        <h3 className="text-lg font-bold text-text-primary mb-2">Integration Guide</h3>
        <p className="text-sm text-text-secondary mb-6">
          Your Dronzer Gateway is 100% OpenAI-compatible. Use standard OpenAI SDKs and simply override the base URL.
        </p>
        
        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-text-secondary">Python (OpenAI SDK)</span>
            </div>
            <pre className="bg-bg-elevated border border-border-primary rounded-lg p-4 overflow-x-auto text-sm font-mono text-text-primary">
              <code>
{`from openai import OpenAI

client = OpenAI(
  base_url="http://localhost:8000/v1",
  api_key="your_gateway_key"
)

response = client.chat.completions.create(
  model="auto",
  messages=[{"role": "user", "content": "Hello"}]
)`}
              </code>
            </pre>
          </div>
          
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-text-secondary">Node.js (OpenAI SDK)</span>
            </div>
            <pre className="bg-bg-elevated border border-border-primary rounded-lg p-4 overflow-x-auto text-sm font-mono text-text-primary">
              <code>
{`import OpenAI from "openai";

const openai = new OpenAI({
  baseURL: "http://localhost:8000/v1",
  apiKey: "your_gateway_key"
});

const response = await openai.chat.completions.create({
  model: "auto",
  messages: [{ role: "user", content: "Hello" }]
});`}
              </code>
            </pre>
          </div>
        </div>
      </motion.div>

      {/* Create Modal */}
      <Dialog.Root open={isCreateOpen} onOpenChange={setIsCreateOpen}>
        <Dialog.Portal>
          <Dialog.Overlay className="fixed inset-0 bg-bg-overlay backdrop-blur-sm z-50 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />
          <Dialog.Content className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-md glass-card p-6 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95">
            <div className="flex items-center justify-between mb-6">
              <Dialog.Title className="text-lg font-semibold text-text-primary">Generate Gateway Key</Dialog.Title>
              <Dialog.Close asChild>
                <button className="p-1 rounded-lg hover:bg-bg-elevated text-text-tertiary hover:text-text-primary transition-colors">
                  <X className="w-4 h-4" />
                </button>
              </Dialog.Close>
            </div>
            
            <form onSubmit={handleSubmit(handleCreate)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1.5">Key Name (Label)</label>
                <input 
                  {...register("label")} 
                  autoFocus
                  className="input-field w-full h-10" 
                  placeholder="e.g. Mobile App Prod"
                  disabled={createKey.isPending}
                />
                {errors.label && <p className="mt-1.5 text-xs text-error">{errors.label.message}</p>}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1.5">Project Access (Optional)</label>
                <select 
                  {...register("project_id")} 
                  className="input-field w-full h-10 appearance-none bg-[url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20width%3D%2224%22%20height%3D%2224%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cpath%20d%3D%22M7%2010l5%205%205-5z%22%20fill%3D%22%236b7280%22%2F%3E%3C%2Fsvg%3E')] bg-[length:24px_24px] bg-[right_8px_center] bg-no-repeat"
                  disabled={createKey.isPending || !projects}
                >
                  <option value="">All Projects (Org Level)</option>
                  {projects?.map(p => (
                    <option key={p.id} value={p.id}>{p.name}</option>
                  ))}
                </select>
                <p className="mt-1.5 text-xs text-text-tertiary">
                  If selected, this key can only route traffic to this specific project.
                </p>
                {errors.project_id && <p className="mt-1.5 text-xs text-error">{errors.project_id.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1.5">Task Type</label>
                <select 
                  {...register("task_type")} 
                  className="input-field w-full h-10 appearance-none bg-[url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20width%3D%2224%22%20height%3D%2224%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cpath%20d%3D%22M7%2010l5%205%205-5z%22%20fill%3D%22%236b7280%22%2F%3E%3C%2Fsvg%3E')] bg-[length:24px_24px] bg-[right_8px_center] bg-no-repeat"
                  disabled={createKey.isPending}
                >
                  <option value="chat">General Chat (Default)</option>
                  <option value="coding">Coding & Development</option>
                  <option value="reasoning">Complex Reasoning / Math</option>
                  <option value="vision">Multimodal / Vision</option>
                  <option value="embedding">Vector Embeddings</option>
                </select>
                <p className="mt-1.5 text-xs text-text-tertiary">
                  We use this to strictly route requests using this key to the optimal model architecture.
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1.5">Custom Model Priorities (Optional)</label>
                <div className="flex gap-2 mb-2">
                  <select 
                    className="input-field flex-1 h-10 appearance-none bg-[url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20width%3D%2224%22%20height%3D%2224%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cpath%20d%3D%22M7%2010l5%205%205-5z%22%20fill%3D%22%236b7280%22%2F%3E%3C%2Fsvg%3E')] bg-[length:24px_24px] bg-[right_8px_center] bg-no-repeat"
                    onChange={handleAddModel}
                    value=""
                    disabled={createKey.isPending}
                  >
                    <option value="" disabled>Add model to priority list...</option>
                    {availableModels.map(m => (
                      <option key={m.id} value={m.id}>{m.name} ({m.provider_id})</option>
                    ))}
                  </select>
                </div>
                
                {modelPriorities.length > 0 && (
                  <div className="space-y-2 border border-border-primary rounded-lg p-3 bg-bg-primary max-h-48 overflow-y-auto">
                    {modelPriorities.map((mId, index) => {
                      const m = allModels?.find(x => x.id === mId);
                      return (
                        <div key={mId} className="flex items-center justify-between p-2 rounded bg-bg-elevated border border-border-primary">
                          <span className="text-sm text-text-primary">
                            <span className="text-text-tertiary mr-2">{index + 1}.</span> 
                            {m?.name || mId}
                          </span>
                          <div className="flex items-center gap-1">
                            <button type="button" onClick={() => moveModelUp(index)} disabled={index === 0} className="p-1 rounded hover:bg-bg-card-hover disabled:opacity-30"><ArrowUp className="w-3 h-3" /></button>
                            <button type="button" onClick={() => moveModelDown(index)} disabled={index === modelPriorities.length - 1} className="p-1 rounded hover:bg-bg-card-hover disabled:opacity-30"><ArrowDown className="w-3 h-3" /></button>
                            <button type="button" onClick={() => removeModel(index)} className="p-1 rounded hover:bg-error-muted text-error ml-1"><X className="w-3 h-3" /></button>
                          </div>
                        </div>
                      )
                    })}
                  </div>
                )}
                <p className="mt-1.5 text-xs text-text-tertiary">
                  Requests using this key will try these models exactly in this order. If all fail, it falls back to the global pool.
                </p>
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
                  Generate Key
                </button>
              </div>
            </form>
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>

      {/* Newly Created Key Modal */}
      <Dialog.Root open={!!newlyCreatedKey} onOpenChange={(open) => !open && setNewlyCreatedKey(null)}>
        <Dialog.Portal>
          <Dialog.Overlay className="fixed inset-0 bg-bg-overlay backdrop-blur-sm z-50 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />
          <Dialog.Content className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-md glass-card p-6 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95">
            <div className="flex flex-col items-center text-center space-y-4">
              <div className="w-12 h-12 rounded-full bg-success-muted flex items-center justify-center">
                <Key className="w-6 h-6 text-success" />
              </div>
              <h2 className="text-xl font-bold text-text-primary">Save Your API Key</h2>
              <p className="text-sm text-text-secondary">
                Please copy your Gateway API key now. For your security, it will not be shown again.
              </p>
              
              <div className="w-full flex items-center mt-4">
                <input 
                  type="text"
                  readOnly
                  value={newlyCreatedKey || ""}
                  className="input-field h-12 w-full font-mono text-sm pr-12 text-accent-primary bg-bg-primary"
                />
                <button 
                  onClick={() => copyToClipboard(newlyCreatedKey || "")}
                  className="absolute right-8 p-2 text-text-tertiary hover:text-accent-primary transition-colors"
                >
                  <Copy className="w-4 h-4" />
                </button>
              </div>

              <div className="pt-4 w-full">
                <button 
                  onClick={() => setNewlyCreatedKey(null)}
                  className="w-full px-4 py-2 rounded-lg text-sm font-medium text-white gradient-accent hover:opacity-90"
                >
                  I&apos;ve Saved It
                </button>
              </div>
            </div>
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>

      {/* Delete Confirmation */}
      <ConfirmationModal
        open={!!keyToRevoke}
        onOpenChange={(open) => !open && setKeyToRevoke(null)}
        title="Revoke Gateway Key"
        description={`Are you sure you want to revoke the key "${keyToRevoke?.label}"? Any applications using it to connect to Dronzer will immediately lose access.`}
        variant="danger"
        confirmLabel="Revoke Key"
        onConfirm={handleRevoke}
        loading={revokeKey.isPending}
      />
    </div>
  );
}
