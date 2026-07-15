"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { motion, AnimatePresence } from "framer-motion";
import * as Dialog from "@radix-ui/react-dialog";
import { Building2, Plus, Trash2, Check, Search, Mail, Loader2, X } from "lucide-react";

import { useOrganizations, useCreateOrg, useDeleteOrg } from "@/lib/hooks/use-organizations";
import { useAppStore } from "@/lib/stores/app-store";
import { StatusPill } from "@/components/ui/status-pill";
import { EmptyState } from "@/components/ui/empty-state";
import { ConfirmationModal } from "@/components/ui/confirmation-modal";
import { SkeletonCard } from "@/components/ui/skeleton";
import type { OrganizationResponse } from "@/lib/api/types";

const orgSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  billing_email: z.string().email("Invalid email").optional().or(z.literal("")),
});
type OrgForm = z.infer<typeof orgSchema>;

export default function OrganizationsPage() {
  const { data: orgs, isLoading } = useOrganizations();
  const { activeOrganization, setActiveOrg } = useAppStore();
  const createOrg = useCreateOrg();
  const deleteOrg = useDeleteOrg();

  const [search, setSearch] = useState("");
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [orgToDelete, setOrgToDelete] = useState<OrganizationResponse | null>(null);

  const { register, handleSubmit, reset, formState: { errors } } = useForm<OrgForm>({
    resolver: zodResolver(orgSchema),
    defaultValues: { name: "", billing_email: "" }
  });

  const filteredOrgs = orgs?.filter(o => o.name.toLowerCase().includes(search.toLowerCase())) || [];

  const handleCreate = async (data: OrgForm) => {
    try {
      await createOrg.mutateAsync(data);
      setIsCreateOpen(false);
      reset();
    } catch (e) {
      // handled by mutation onError
    }
  };

  const handleDelete = async () => {
    if (!orgToDelete) return;
    try {
      await deleteOrg.mutateAsync(orgToDelete.id);
      if (activeOrganization?.id === orgToDelete.id) {
        setActiveOrg(null);
      }
    } catch (e) {
      // handled by mutation onError
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row gap-4 sm:items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-text-primary tracking-tight">Organizations</h2>
          <p className="text-sm text-text-secondary mt-1">Manage tenants and billing entities.</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-tertiary" />
            <input 
              type="text" 
              placeholder="Search organizations..." 
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
            <span className="hidden sm:inline">Create Org</span>
          </button>
        </div>
      </div>

      {/* Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, i) => <SkeletonCard key={i} />)}
        </div>
      ) : filteredOrgs.length === 0 ? (
        <EmptyState 
          icon={Building2}
          title={search ? "No organizations found" : "No organizations yet"}
          description={search ? `No results for "${search}"` : "Create your first organization to get started with Dronzer AI Gateway."}
          action={
            !search && (
              <button 
                onClick={() => setIsCreateOpen(true)}
                className="px-4 py-2 rounded-lg gradient-accent text-white text-sm font-medium"
              >
                Create Organization
              </button>
            )
          }
        />
      ) : (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          {filteredOrgs.map((org, i) => {
            const isActive = activeOrganization?.id === org.id;
            
            return (
              <motion.div 
                key={org.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className="glass-card hover:glass-card-hover p-6 flex flex-col transition-all group"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-bg-elevated flex items-center justify-center border border-border-primary">
                      <Building2 className="w-5 h-5 text-text-secondary" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-text-primary text-base truncate max-w-[150px]">{org.name}</h3>
                      <StatusPill status={org.is_active ? "active" : "inactive"} className="mt-1" />
                    </div>
                  </div>
                  
                  <button 
                    onClick={() => setOrgToDelete(org)}
                    className="p-2 text-text-tertiary hover:text-error hover:bg-error-muted rounded-lg opacity-0 group-hover:opacity-100 transition-all focus:opacity-100 focus:outline-none"
                    title="Delete Organization"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
                
                <div className="space-y-3 mb-6 flex-1">
                  <div className="flex items-center gap-2 text-sm text-text-secondary">
                    <Mail className="w-4 h-4 text-text-tertiary" />
                    <span className="truncate">{org.billing_email || <span className="text-text-muted italic">No billing email</span>}</span>
                  </div>
                  <div className="text-xs text-text-tertiary">
                    Created on {new Date(org.created_at).toLocaleDateString()}
                  </div>
                </div>
                
                <button
                  onClick={() => setActiveOrg(org)}
                  disabled={isActive}
                  className={`w-full py-2 rounded-lg text-sm font-medium transition-all flex items-center justify-center gap-2
                    ${isActive 
                      ? "bg-accent-muted text-accent-primary cursor-default border border-accent-primary/20" 
                      : "bg-bg-elevated text-text-secondary hover:text-text-primary hover:border-border-secondary border border-border-primary"
                    }`}
                >
                  {isActive ? (
                    <>
                      <Check className="w-4 h-4" /> Active Context
                    </>
                  ) : "Set as Active"}
                </button>
              </motion.div>
            );
          })}
        </motion.div>
      )}

      {/* Create Modal */}
      <Dialog.Root open={isCreateOpen} onOpenChange={setIsCreateOpen}>
        <Dialog.Portal>
          <Dialog.Overlay className="fixed inset-0 bg-bg-overlay backdrop-blur-sm z-50 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />
          <Dialog.Content className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-md glass-card p-6 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95">
            <div className="flex items-center justify-between mb-6">
              <Dialog.Title className="text-lg font-semibold text-text-primary">Create Organization</Dialog.Title>
              <Dialog.Close asChild>
                <button className="p-1 rounded-lg hover:bg-bg-elevated text-text-tertiary hover:text-text-primary transition-colors">
                  <X className="w-4 h-4" />
                </button>
              </Dialog.Close>
            </div>
            
            <form onSubmit={handleSubmit(handleCreate)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1.5">Organization Name</label>
                <input 
                  {...register("name")} 
                  autoFocus
                  className="input-field w-full h-10" 
                  placeholder="Acme Corp"
                  disabled={createOrg.isPending}
                />
                {errors.name && <p className="mt-1.5 text-xs text-error">{errors.name.message}</p>}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1.5">Billing Email <span className="text-text-muted font-normal">(optional)</span></label>
                <input 
                  {...register("billing_email")} 
                  className="input-field w-full h-10" 
                  placeholder="billing@acme.com"
                  disabled={createOrg.isPending}
                />
                {errors.billing_email && <p className="mt-1.5 text-xs text-error">{errors.billing_email.message}</p>}
              </div>
              
              <div className="pt-4 flex justify-end gap-3">
                <Dialog.Close asChild>
                  <button type="button" className="px-4 py-2 rounded-lg text-sm font-medium bg-bg-elevated border border-border-primary text-text-secondary hover:text-text-primary">
                    Cancel
                  </button>
                </Dialog.Close>
                <button 
                  type="submit" 
                  disabled={createOrg.isPending}
                  className="px-4 py-2 rounded-lg text-sm font-medium text-white gradient-accent hover:opacity-90 flex items-center gap-2 disabled:opacity-70"
                >
                  {createOrg.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
                  Create
                </button>
              </div>
            </form>
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>

      {/* Delete Confirmation */}
      <ConfirmationModal
        open={!!orgToDelete}
        onOpenChange={(open) => !open && setOrgToDelete(null)}
        title="Delete Organization"
        description={`Are you sure you want to delete "${orgToDelete?.name}"? This action cannot be undone and will delete all associated projects and API keys.`}
        variant="danger"
        confirmLabel="Delete Organization"
        onConfirm={handleDelete}
        loading={deleteOrg.isPending}
      />
    </div>
  );
}
